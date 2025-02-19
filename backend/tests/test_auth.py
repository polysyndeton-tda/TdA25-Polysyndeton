
import unittest
from src import app, db
from config import Config
from src.models import create_superuser


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.drop_all()
            db.create_all()
            create_superuser()

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

    def test_admin_can_login(self):
        credentials = {"username" : Config.SUPERUSER_USERNAME, "password": Config.SUPERUSER_PASSWORD}

        login_response = self.app.post('/api/v1/login', json=credentials) 

        self.assertEqual(login_response.status, "200 OK")

    def test_register_w_admin_credentails_impossible(self):
        credentials = {"username" : Config.SUPERUSER_USERNAME, "password": Config.SUPERUSER_PASSWORD, "email": Config.SUPERUSER_EMAIL, "elo": 0}
        
        response = self.app.post('/api/v1/users', json=credentials) 

        self.assertEqual(response.status, "409 CONFLICT")