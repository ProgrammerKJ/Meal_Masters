import unittest
from app import app, db
from models import User, Recipe, SavedRecipe, WeightEntry
from datetime import date

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  


if __name__ == '__main__':
    unittest.main()
