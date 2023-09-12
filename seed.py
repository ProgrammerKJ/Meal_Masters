from app import app, db
from models import User, SavedRecipe, WeightEntry, Recipe

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User.signup("user1", "user1@example.com", "password1")
    user2 = User.signup("user2", "user2@example.com", "password2")

    db.session.add_all([user1, user2])
    db.session.commit()

    saved_recipe1 = SavedRecipe(user_id=user1.user_id, recipe_id=1)
    saved_recipe2 = SavedRecipe(user_id=user2.user_id, recipe_id=2)

    db.session.add_all([saved_recipe1, saved_recipe2])
    db.session.commit()

    weight_entry1 = WeightEntry(
        user_id=user1.user_id, date="2023-01-01", weight=150, goal_weight=140)
    weight_entry2 = WeightEntry(
        user_id=user2.user_id, date="2023-01-01", weight=160, goal_weight=150)

    db.session.add_all([weight_entry1, weight_entry2])
    db.session.commit()

    recipe1 = Recipe(recipe_id=1)
    recipe2 = Recipe(recipe_id=2)

    db.session.add_all([recipe1, recipe2])
    db.session.commit()
