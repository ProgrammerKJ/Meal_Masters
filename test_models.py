import unittest
from app import app, db, User, SavedRecipe, WeightEntry, Recipe

class TestModels(unittest.TestCase):
    def setUp(self):
    
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lukadon1996$@localhost/fitness_app'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

        self.client = app.test_client()
        self.app_context = app.app_context() 
        self.app_context.push()  
        db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

        self.app_context.pop() 

    def test_user_model(self):
        
        user = User.signup('testuser', 'test@example.com', 'password')
        db.session.commit()

        queried_user = User.query.filter_by(username='testuser').first()

        self.assertEqual(user, queried_user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password'))

    def test_saved_recipe_model(self):
        user = User.signup('testuser', 'test@example.com', 'password')
        db.session.commit()

        saved_recipe = SavedRecipe(user_id=user.user_id, recipe_id=1)
        db.session.add(saved_recipe)
        db.session.commit()

        queried_recipe = SavedRecipe.query.first()

        self.assertEqual(saved_recipe, queried_recipe)
        self.assertEqual(saved_recipe.user_id, user.user_id)
        self.assertEqual(saved_recipe.recipe_id, 1)

    def test_weight_entry_model(self):
        user = User.signup('testuser', 'test@example.com', 'password')
        db.session.commit()

        weight_entry = WeightEntry(user_id=user.user_id, date='2023-09-12', weight=70.5, goal_weight=65.0)
        db.session.add(weight_entry)
        db.session.commit()

        queried_entry = WeightEntry.query.first()

        self.assertEqual(weight_entry, queried_entry)
        self.assertEqual(weight_entry.user_id, user.user_id)
        self.assertEqual(str(weight_entry.date), '2023-09-12')
        self.assertEqual(weight_entry.weight, 70.5)
        self.assertEqual(weight_entry.goal_weight, 65.0)

    def test_recipe_model(self):
        recipe = Recipe()
        db.session.add(recipe)
        db.session.commit()

        queried_recipe = Recipe.query.first()

        self.assertEqual(recipe, queried_recipe)
