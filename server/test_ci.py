import pyrebase
import pytest

from firebase import Firebase
from app import app


# Need a dummy test to ensure that pytest doesn't fail during CI/CD
def test_ci():
    assert True


# App setup
# @pytest.fixture()
# def app():
#     app = Flask(__name__)
#     app.secret_key = "notasecretkey"
#
#     return app.test_client()


@pytest.fixture()
def auth():
    firebaseConfig = {
        'apiKey': "AIzaSyDIZ0eIPqRIN4coI_TvULQZ3m_wSXqUkZE",
        'authDomain': "codecrushers-83ba1.firebaseapp.com",
        'databaseURL': "https://codecrushers-83ba1-default-rtdb.firebaseio.com",
        'projectId': "codecrushers-83ba1",
        'storageBucket': "codecrushers-83ba1.appspot.com",
        'messagingSenderId': "611473793281",
        'appId': "1:611473793281:web:f2fa45a46286a1fed6fb00",
        'measurementId': "G-6JX1R48Z3J"
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    return auth


@pytest.fixture()
def db():
    db = Firebase()
    db.initialize("firebase_cfg.json")
    return db


# Test that the app is running
def test_web_app_running():
    """
    GIVEN a web app
    WHEN requesting the /hello endpoint
    THEN check response code is 200 and data is 'Hello, World!'
    """
    response = app.test_client().get('/hello')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, World!'


# Test home endpoint
def test_home_endpoint():
    response = app.test_client().get('/')
    assert response.status_code == 200

# Test login endpoint
def test_login_endpoint():
    response = app.test_client().get('/login')
    assert response.status_code == 200

# Test signup endpoint
def test_signup_endpoint():
    response = app.test_client().get('/signup')
    assert response.status_code == 200

# Test logout endpoint
def test_logout_endpoint():
    with app.test_client() as client:
        # Logout a user that is logged in
        with client.session_transaction() as session:
            session['user'] = 'nobobjam@gmail.com'
        response = client.get('/logout')
        assert response.status_code == 200
        # Logout when no user is logged in
        with client.session_transaction() as session:
            session['user'] = 'nobobjam@gmail.com'
            session.pop('user')
        response = client.get('/logout')
        assert response.status_code == 200

# Test for the creation of a user with email and password
def test_user_creation(auth):
    email = "placeholder@provider.com"
    password = "123456"
    user = auth.create_user_with_email_and_password(email, password)
    assert isinstance(user, dict)
    auth.delete_user_account(user['idToken'])

# Test for user login
def test_user_login(auth):
    email = "nobobjam@gmail.com"
    password = "123456"
    user = auth.sign_in_with_email_and_password(email, password)
    assert isinstance(user, dict)

