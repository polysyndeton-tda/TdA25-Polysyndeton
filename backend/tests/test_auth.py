
import unittest
from src import app, db


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_register_login_single_user(self):
        credentials = {"username" : "hrac", "password": "tajneheslo", "email": "a@b.com", "elo": 400}

        _ = self.app.post('/api/v1/users', json=credentials) 
        login_response = self.app.post('/api/v1/login', json=credentials) 

        self.assertEqual(login_response.status, "200 OK")
        self.assertTrue(b"token" in login_response.data)

    def test_no_register_login_single_user(self):
        credentials = {"username" : "hrac", "password": "tajneheslo", "email": "a@b.com", "elo": 400}

        login_response = self.app.post('/api/v1/login', json=credentials) 

        self.assertEqual(login_response.status, "404 NOT FOUND")