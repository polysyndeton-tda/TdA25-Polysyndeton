from src import app, db, socketio
from flask_socketio import SocketIOTestClient
import unittest
from src.models import User
from src.matchmaking import get_room_name
from src.routes import active_rooms
import time


class TestFriendlyMatch(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.drop_all()
            db.create_all()

            self.user1 = User(username="player1", email="p1@example.com", elo=1001)
            self.user1.set_password("123")
            db.session.add(self.user1)

            self.user2 = User(username="player2", email="p2@example.com", elo=1010)
            self.user2.set_password("123")
            db.session.add(self.user2)

            db.session.commit()

            self.user1_uuid = self.user1.uuid
            self.user2_uuid = self.user2.uuid
            self.room = get_room_name(self.user1_uuid, self.user2_uuid)

        self.socket_client1 = SocketIOTestClient(
            app, socketio, query_string=f"user_uuid={self.user1.uuid}"
        )

        self.socket_client2 = SocketIOTestClient(
            app, socketio, query_string=f"user_uuid={self.user2.uuid}"
        )
        self.socket_client1.connect()
        self.socket_client2.connect()

    def tearDown(self):
        try:
            self.socket_client1.disconnect()
        except (ConnectionError, AttributeError) as e:
            print(f"Error disconnecting client 1: {e}")

        try:
            self.socket_client2.disconnect()
        except (ConnectionError, AttributeError) as e:
            print(f"Error disconnecting client 2: {e}")

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_friendly_match_invitation(self):
        response = self.app.post(
            "/api/v1/friendly",
            json={"user_uuid": self.user1_uuid, "opponent_uuid": self.user2_uuid},
        )

        self.assertEqual(response.status_code, 200)

        # Check if opponent received the invitatio
        received = self.socket_client2.get_received()
        self.assertTrue(any(event["name"] == "game_invitation" for event in received))

        invitation = next(
            event for event in received if event["name"] == "game_invitation"
        )
        self.assertEqual(invitation["args"][0]["challenger"]["uuid"], self.user1_uuid)

    def test_friendly_match_accept(self):
        """Test accepting a friendly match invitation"""
        # Join both players to the room
        self.socket_client1.emit(
            "join_friendly", {"username": "player1", "room": self.room}
        )
        self.socket_client2.emit(
            "join_friendly", {"username": "player2", "room": self.room}
        )

        # Clear previous messages
        self.socket_client1.get_received()
        self.socket_client2.get_received()

        # Player 2 accepts the game
        self.socket_client2.emit(
            "accept_game", {"room": self.room, "username": "player2"}
        )

        time.sleep(1)

        # Check if both players received game acceptance and start
        received1 = self.socket_client1.get_received()
        received2 = self.socket_client2.get_received()

        self.assertTrue(any(event["name"] == "game_accepted" for event in received1))
        self.assertTrue(any(event["name"] == "game_start" for event in received1))
        self.assertTrue(any(event["name"] == "game_accepted" for event in received2))
        self.assertTrue(any(event["name"] == "game_start" for event in received2))

    def test_friendly_match_decline(self):
        """Test declining a friendly match invitation"""
        # Join both players to the room
        self.socket_client1.emit(
            "join_friendly", {"username": "player1", "room": self.room}
        )
        self.socket_client2.emit(
            "join_friendly", {"username": "player2", "room": self.room}
        )

        # Clear previous messages
        self.socket_client1.get_received()
        self.socket_client2.get_received()

        # Player 2 declines the game
        self.socket_client2.emit(
            "decline_game", {"room": self.room, "username": "player2"}
        )

        time.sleep(1)

        # Check if both players received decline notification
        received1 = self.socket_client1.get_received()
        received2 = self.socket_client2.get_received()

        self.assertTrue(any(event["name"] == "game_declined" for event in received1))
        self.assertTrue(any(event["name"] == "game_declined" for event in received2))

        self.assertNotIn(self.room, active_rooms)
