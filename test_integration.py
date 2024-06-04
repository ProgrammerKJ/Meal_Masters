import pytest
from app import app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lukadon1996$@localhost/fitness_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_saved_recipe_integration(test_client):
    # Simulate user signup
    signup_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }
    response = test_client.post('/signup', data=signup_data, follow_redirects=True)
    assert response.status_code == 200  

    # Simulate adding a recipe to saved recipes
    login_data = {
        'username': 'testuser',
        'password': 'password'
    }
    response = test_client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200  

    save_recipe_response = test_client.post('/save_recipe/1', follow_redirects=True) 
    assert save_recipe_response.status_code in [200, 302] 

    # Simulate viewing saved recipes
    view_saved_response = test_client.get('/saved_recipes')
    assert view_saved_response.status_code in [200, 302]  

def test_user_signup_and_login(test_client):
    # Simulate user signup
    signup_data = {
        'username': 'testuser333',
        'email': 'test@example.com',
        'password': 'password'
    }
    response = test_client.post('/signup', data=signup_data, follow_redirects=True)
    assert response.status_code == 200  

    # Simulate user login
    login_data = {
        'username': 'testuser333',
        'password': 'password'
    }
    response = test_client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200 
    assert b'testuser333' in response.data  

def test_weight_entry_integration(test_client):
    # Simulate user signup
    signup_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }
    response = test_client.post('/signup', data=signup_data, follow_redirects=True)
    assert response.status_code == 200  

    # Simulate user login
    login_data = {
        'username': 'testuser',
        'password': 'password'
    }
    response = test_client.post('/login', data=login_data, follow_redirects=True)
    assert response.status_code == 200  

    # Check if logged in
    assert b'testuser' in response.data  

    # Simulate adding weight entry
    weight_entry_data = {
        'date': '2023-09-12',
        'weight': 70.5,
        'goal_weight': 65.0
    }
    response = test_client.post('/weight_entry', data=weight_entry_data, follow_redirects=True)
    assert response.status_code == 200  

    # Simulate viewing weight tracker
    view_weight_tracker_response = test_client.get('/weight_tracker', follow_redirects=True)
    assert view_weight_tracker_response.status_code == 200  
