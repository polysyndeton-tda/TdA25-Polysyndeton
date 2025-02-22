import unittest
from flask_socketio import SocketIOTestClient
from src import app, db, socketio
from src.models import User
from src.routes import active_rooms
from src.matchmaking import get_room_name
import time


class TestMatch(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.socket_client1 = SocketIOTestClient(app, socketio)
        self.socket_client2 = SocketIOTestClient(app, socketio)
        self.socket_client1.connect()
        self.socket_client2.connect()

        with app.app_context():
            db.drop_all()
            db.create_all()

            self.user1 = User(username="player1", email="p1@eg.com", elo=1001)
            self.user1.set_password("123")
            db.session.add(self.user1)

            self.user2 = User(username="player2", email="p2@eg.com", elo=1010)
            self.user2.set_password("123")
            db.session.add(self.user2)

            db.session.commit()

            self.user1_uuid = self.user1.uuid
            self.user2_uuid = self.user2.uuid

            self.room = get_room_name(self.user1_uuid, self.user2_uuid)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_matchmaking_pairing(self):
        with app.app_context():
            user1 = User.query.filter_by(uuid=self.user1_uuid).first()
            user2 = User.query.filter_by(uuid=self.user2_uuid).first()

            response1 = self.app.post("/api/v1/matchmaking", json={"uuid": user1.uuid})
            self.assertEqual(response1.status_code, 200)
            response2 = self.app.post("/api/v1/matchmaking", json={"uuid": user2.uuid})
            self.assertEqual(response2.status_code, 200)

    def test_game_join(self):
        self.socket_client1.emit("join", {"username": "player1", "room": self.room})

        self.socket_client2.emit("join", {"username": "player2", "room": self.room})

        time.sleep(1)

        self.assertIn(self.room, active_rooms)
        self.assertEqual(len(active_rooms[self.room]), 2)

        received = self.socket_client1.get_received()
        self.assertTrue(any(event["name"] == "game_start" for event in received))

        self.socket_client1.disconnect()
        self.socket_client2.disconnect()

    def test_game_moves(self):
        self.socket_client1.emit("join", {"username": "player1", "room": self.room})
        self.socket_client2.emit("join", {"username": "player2", "room": self.room})

        self.socket_client1.get_received()
        self.socket_client2.get_received()

        move_data = {
            "room": self.room,
            "move": [0, 0],
            "username": "player1",
            "symbol": "X",
        }
        self.socket_client1.emit("move", move_data)

        time.sleep(1)

        received = self.socket_client2.get_received()
        self.assertTrue(any(event["name"] == "move" for event in received))
        move_event = next(event for event in received if event["name"] == "move")
        self.assertEqual(move_event["args"][0], move_data)

        self.socket_client1.disconnect()
        self.socket_client2.disconnect()

    def test_player_disconnect(self):
        self.socket_client1.emit("join", {"username": "player1", "room": self.room})
        self.socket_client2.emit("join", {"username": "player2", "room": self.room})

        self.socket_client1.get_received()
        self.socket_client2.get_received()

        self.socket_client1.disconnect()

        time.sleep(1)

        received = self.socket_client2.get_received()
        self.assertTrue(
            any(event["name"] == "opponent_disconnected" for event in received)
        )

        self.assertEqual(len(active_rooms[self.room]), 1)

        self.socket_client2.disconnect()

    def test_multiple_games(self):
        with app.app_context():
            user3 = User(username="player3", email="p3@eg.com", elo=1020)
            user3.set_password("123")
            db.session.add(user3)

            user4 = User(username="player4", email="p4@eg.com", elo=1030)
            user4.set_password("123")
            db.session.add(user4)

            db.session.commit()

            room2 = get_room_name(user3.uuid, user4.uuid)

        socket_client3 = SocketIOTestClient(app, socketio)
        socket_client4 = SocketIOTestClient(app, socketio)
        socket_client3.connect()
        socket_client4.connect()

        move_data = {}

        try:
            self.socket_client1.emit("join", {"username": "player1", "room": self.room})
            self.socket_client2.emit("join", {"username": "player2", "room": self.room})
            socket_client3.emit("join", {"username": "player3", "room": room2})
            socket_client4.emit("join", {"username": "player4", "room": room2})

            time.sleep(1)

            self.assertEqual(len(active_rooms), 2)
            self.assertEqual(len(active_rooms[self.room]), 2)
            self.assertEqual(len(active_rooms[room2]), 2)

            move_data = {
                "room": self.room,
                "move": [0, 0],
                "username": "player1",
                "symbol": "X",
            }
            self.socket_client1.emit("move", move_data)

            time.sleep(1)

            received2 = self.socket_client2.get_received()
            received3 = socket_client3.get_received()
            received4 = socket_client4.get_received()

            self.assertTrue(any(event["name"] == "move" for event in received2))
            self.assertFalse(any(event["name"] == "move" for event in received3))
            self.assertFalse(any(event["name"] == "move" for event in received4))

        finally:
            self.socket_client1.emit("move", move_data)
            self.socket_client1.disconnect()
            self.socket_client2.disconnect()
            socket_client3.disconnect()
