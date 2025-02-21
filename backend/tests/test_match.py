import unittest
from flask_socketio import SocketIOTestClient
from src import app, db, socketio
from config import Config
from src.models import User, create_superuser
from src.routes import q, matchmaking, active_rooms
import time

class TestMatch(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.socket_client = SocketIOTestClient(app, socketio)

        with app.app_context():
            db.drop_all()
            db.create_all()

            self.user1 = User(username='player1', email='p1@example.com', elo=1001)
            self.user1.set_password("123")

            self.user2 = User(username='player2', email='p2@example.com', elo=1010)
            self.user2.set_password("123")

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.socket_client.disconnect()

    def test_matchmaking_pairing(self):
        with app.app_context():
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.commit()

            matchmaking.add_user(self.user1)
            matchmaking.add_user(self.user2)

            db.session.refresh(self.user1)
            db.session.refresh(self.user2)

            paired_user = matchmaking.find_closest_user(self.user1)
            
            self.assertEqual(paired_user.username, self.user2.username)

    def test_socket_join(self):
        room = "test_room"
        self.socket_client.emit("join", {"username": "player1", "room": room})
        received = self.socket_client.get_received()

        print(received)
        self.assertTrue(any(event["name"] == "join" for event in received))