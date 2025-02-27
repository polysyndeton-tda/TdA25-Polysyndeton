from src import app, db, socketio
from flask_socketio import SocketIOTestClient
import unittest
from src.matchmaking import get_room_name
from src.routes import active_rooms, friendly_sessions
import time
import uuid


class TestFriendlyMatch(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.player1_name = "abc"
        self.player2_name = "def"
        self.room = str(uuid.uuid4())

        self.socket_client1 = SocketIOTestClient(app, socketio)
        self.socket_client2 = SocketIOTestClient(app, socketio)
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

    def test_friendly_match_invitation(self):
        response = self.app.post(
            "/api/v1/friendly",
            json={"user_name": self.player1_name, "opponent_name": self.player2_name},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("room", data)
        self.room = data["room"] # id generated from the request

        with app.app_context():
            self.assertIn(self.room, friendly_sessions)
            self.assertEqual(friendly_sessions[self.room]["player1"], self.player1_name)
            self.assertEqual(friendly_sessions[self.room]["player2"], self.player2_name)

    def test_friendly_match_accept(self):
        with app.app_context(): # result of friendly POST
            friendly_sessions[self.room] = {
                "player1": self.player1_name,
                "player2": self.player2_name,
            }

        self.socket_client1.emit(
            "join_friendly", {"username": self.player1_name, "room": self.room}
        )
        self.socket_client2.emit(
            "join_friendly", {"username": self.player2_name, "room": self.room}
        )

        self.socket_client2.emit(
            "accept_game", {"room": self.room, "username": self.player2_name}
        )

        time.sleep(1)

        received1 = self.socket_client1.get_received()
        received2 = self.socket_client2.get_received()

        self.assertTrue(any(event["name"] == "game_start" for event in received1))
        self.assertTrue(any(event["name"] == "game_start" for event in received2))

        game_start_event = next(event for event in received1 if event["name"] == "game_start")
        self.assertEqual(game_start_event["args"][0]["symbols"][self.player1_name], "X")
        self.assertEqual(game_start_event["args"][0]["symbols"][self.player2_name], "O")

    def test_friendly_match_decline(self):
        with app.app_context():
            friendly_sessions[self.room] = {
                "player1": self.player1_name,
                "player2": self.player2_name,
            }

        self.socket_client1.emit(
            "join_friendly", {"username": self.player1_name, "room": self.room}
        )
        self.socket_client2.emit(
            "join_friendly", {"username": self.player2_name, "room": self.room}
        )

        self.socket_client2.emit(
            "decline_game", {"room": self.room, "username": self.player2_name}
        )

        time.sleep(1)

        received1 = self.socket_client1.get_received()
        received2 = self.socket_client2.get_received()

        self.assertTrue(any(event["name"] == "game_declined" for event in received1))
        self.assertTrue(any(event["name"] == "game_declined" for event in received2))

        self.assertNotIn(self.room, active_rooms)
        with app.app_context():
            self.assertNotIn(self.room, friendly_sessions)

    def test_invalid_room_join(self):
        invalid_room = "invalid-room-id"
        self.socket_client1.emit(
            "join_friendly", {"username": self.player1_name, "room": invalid_room}
        )

        time.sleep(1)

        received1 = self.socket_client1.get_received()
        self.assertTrue(any(event["name"] == "error" for event in received1))
        error_event = next(event for event in received1 if event["name"] == "error")
        self.assertEqual(error_event["args"][0]["message"], "Invalid friendly room")

    def test_unauthorized_join(self):
        with app.app_context():
            friendly_sessions[self.room] = {
                "player1": self.player1_name,
                "player2": self.player2_name,
            }

        unauthorized_user = "xyz"
        self.socket_client1.emit(
            "join_friendly", {"username": unauthorized_user, "room": self.room}
        )

        time.sleep(1)

        received1 = self.socket_client1.get_received()
        self.assertTrue(any(event["name"] == "error" for event in received1))
        error_event = next(event for event in received1 if event["name"] == "error")
        self.assertEqual(error_event["args"][0]["message"], "Unauthorized access")


if __name__ == "__main__":
    unittest.main()