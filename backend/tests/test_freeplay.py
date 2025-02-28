import unittest
from flask_socketio import SocketIOTestClient
from src import app, db, socketio
import time
import random

class TestFreeplay(unittest.TestCase):
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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        
        try:
            if self.socket_client1.is_connected():
                self.socket_client1.disconnect()
            if self.socket_client2.is_connected():
                self.socket_client2.disconnect()
        except RuntimeError:
            pass

    def test_join_and_play_freeplay(self):
        response = self.app.post('/api/v1/freeplay/create')
        code = response.get_json()['code']

        self.socket_client1.emit('join_freeplay', {'code': code, 'username': 'Player1'})
        time.sleep(1)
        
        self.socket_client2.emit('join_freeplay', {'code': code, 'username': 'Player2'})
        time.sleep(1)

        received1 = self.socket_client1.get_received()
        game_start_event = next(e for e in received1 if e['name'] == 'game_start')
        symbols = game_start_event['args'][0]['symbols']
        
        self.assertEqual(set(symbols.keys()), {'Player1', 'Player2'})
        self.assertEqual(sorted(symbols.values()), ['O', 'X'])

        test_move = [1, 1]
        self.socket_client1.emit('move_freeplay', {
            'code': code,
            'move': test_move,
            'username': 'Player1',
            'symbol': symbols['Player1']
        })
        time.sleep(0.5)

        received2 = self.socket_client2.get_received()
        move_event = next(e for e in received2 if e['name'] == 'move')
        self.assertEqual(move_event['args'][0]['move'], test_move)

    def test_disconnect_freeplay(self):
        response = self.app.post('/api/v1/freeplay/create')
        code = response.get_json()['code']
        
        self.socket_client1.emit('join_freeplay', {'code': code, 'username': 'P1'})
        time.sleep(1)
        
        self.socket_client2.emit('join_freeplay', {'code': code, 'username': 'P2'})
        time.sleep(1)

        self.socket_client1.disconnect()
        time.sleep(2)

        received2 = self.socket_client2.get_received()
        disconnect_events = [e for e in received2 if e['name'] == 'opponent_disconnected']
        
        print("Received events for Player2:", received2)
        
        self.assertTrue(len(disconnect_events) > 0, "No disconnect event received")
        self.assertIn('P1', disconnect_events[0]['args'][0]['message'])