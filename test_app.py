from unittest import TestCase
from unittest.mock import patch
from app import app
from models import db, User, FavoriteCharacter
import json

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///disney_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Don't require CSRF for tests
app.config['WTF_CSRF_ENABLED'] = False

class BasicTests(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

        with app.app_context():
            db.create_all()

            user = User(username="test", email="test@test.com", password="test123")
            db.session.add(user)
            db.session.commit()

            self.user = user

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        return self.app.post('/login', data=dict(username="test", password="test123"), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_guest_page(self):
        response = self.app.get('/guest', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_all_characters(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {'data': []}
            response = self.app.get('/characters', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_single_character(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {'data': []}
            response = self.app.get('/character/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)


    def test_search_characters(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {'data': []}
            response = self.app.get('/search?query=test', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

  

    