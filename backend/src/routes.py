from src import app, db, socketio
from flask import jsonify, send_from_directory, request
from datetime import datetime, timezone, timedelta
import random

from src.models import Game, User
from src.utils import (
    string_from_board,
    board_from_string,
    game_json,
    user_json,
)
from src.validators import (
    validate_game_post,
    validate_game_fields,
    validate_user_fields,
    username_is_unique,
    email_is_unique,
)
from src.matchmaking import SortedUsers, get_room_name, uuid_from_roomname
from src.gamestate import get_gamestate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_socketio import emit, join_room, leave_room
from collections import deque
import gevent
from gevent.lock import BoundedSemaphore
import math
import uuid


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


matchmaking_lock = BoundedSemaphore()
active_rooms_lock = BoundedSemaphore()
friendly_sessions_lock = BoundedSemaphore()
freeplay_rooms_lock = BoundedSemaphore()
matchmaking = SortedUsers()
q = deque()
active_rooms = {}
friendly_sessions = {}
freeplay_rooms = {}

def generate_unique_code():
    while True:
        code = str(random.randint(100000, 999999))
        if code not in freeplay_rooms:
            return code

@app.route("/api/v1/freeplay/create", methods=["POST"])
def create_freeplay_game():
    code = generate_unique_code()
    with freeplay_rooms_lock:
        freeplay_rooms[code] = {
            "players": {},
            "status": "waiting"
        }
    return jsonify({"message": "Freeplay game created", "code": code}), 200

@socketio.on("join_freeplay")
def on_join_freeplay(data):
    code = data["code"]
    username = data["username"]
    with freeplay_rooms_lock:
        if code not in freeplay_rooms:
            emit("error", {"message": "Invalid game code"}, room=request.sid)
            return
        if len(freeplay_rooms[code]["players"]) >= 2:
            emit("error", {"message": "Room is full"}, room=request.sid)
            return

        freeplay_rooms[code]["players"][request.sid] = username
        join_room(code)
        emit("joined_freeplay", {"code": code, "username": username}, room=request.sid)

        if len(freeplay_rooms[code]["players"]) == 1:
            emit("waiting_for_opponent", {"code": code}, room=code)
        elif len(freeplay_rooms[code]["players"]) == 2:
            freeplay_rooms[code]["status"] = "playing"

            players = list(freeplay_rooms[code]["players"].values())
            symbols = {
                players[0]: "X",
                players[1]: "O"
            }

            emit("game_start", {
                "code": code,
                "symbols": symbols
            }, room=code)

            print(f"Game started in room {code} with symbols: {symbols}")

@socketio.on("move_freeplay")
def handle_move_freeplay(data):
    code = data["code"]
    move = data["move"]
    username = data["username"]
    symbol = data["symbol"]
    if code in freeplay_rooms:
        emit("move", {"move": move, "username": username, "symbol": symbol}, room=code, include_self=False)

@socketio.on("disconnect_freeplay")
def handle_disconnect_freeplay():
    with freeplay_rooms_lock:
        for code, room_data in freeplay_rooms.items():
            if request.sid in room_data["players"]:
                username = room_data["players"][request.sid]
                del room_data["players"][request.sid]

                emit("opponent_disconnected", {"message": f"{username} has disconnected"}, room=code)

                if not room_data["players"]:
                    del freeplay_rooms[code]
                break

@app.route("/api/v1/elo", methods=["POST"])
def update_elo():
    data = request.json
    winner_name = data.get("winner_username")
    defeated_name = data.get("defeated_username")
    draw = data.get("is_draw", False)

    winner = User.query.filter_by(username=winner_name).first()
    defeated = User.query.filter_by(username=defeated_name).first()

    if not winner or not defeated:
        print("one of these users not found",winner, winner_name, defeated, defeated_name, file=sys.stderr)
        return jsonify({"error": "one of the users was not found"}), 404

    # constants
    K_FACTOR = 40
    ALPHA = 0.5
    SCALING_FACTOR = 400

    winner_current_elo = winner.elo
    defeated_current_elo = defeated.elo

    winner_s_a = 1.0 if not draw else 0.5
    defeated_s_a = 0.0 if not draw else 0.5

    if draw:
        winner.draws += 1
        defeated.draws += 1
    else:
        winner.wins += 1
        defeated.losses += 1

    winner_e_a = 1 / (1 + 10 ** ((defeated_current_elo - winner_current_elo) / SCALING_FACTOR))
    defeated_e_a = 1 / (1 + 10 ** ((winner_current_elo - defeated_current_elo) / SCALING_FACTOR))

    winner_w = winner.wins
    winner_d = winner.draws
    winner_l = winner.losses
    winner_ratio = (winner_w + winner_d) / (winner_w + winner_d + winner_l)

    defeated_w = defeated.wins
    defeated_d = defeated.draws
    defeated_l = defeated.losses
    defeated_ratio = (defeated_w + defeated_d) / (defeated_w + defeated_d + defeated_l)

    winner_r_a = winner_current_elo + K_FACTOR * (winner_s_a - winner_e_a) * (1 + ALPHA * (0.5 - winner_ratio))
    defeated_r_a = defeated_current_elo + K_FACTOR * (defeated_s_a - defeated_e_a) * (1 + ALPHA * (0.5 - defeated_ratio))

    winner_r_a = math.ceil(winner_r_a)
    defeated_r_a = math.ceil(defeated_r_a)

    winner.elo = winner_r_a
    defeated.elo = defeated_r_a

    db.session.commit()

    return jsonify({"message": "ELO updated successfully"}), 200

@app.route("/api/v1/matchmaking", methods=["POST"])
def matchmaking_request():
    data = request.json
    user_uuid = data.get("uuid")
    queried_user = User.query.filter_by(uuid=user_uuid).first()

    if not queried_user:
        return jsonify({"message": "User not found"}), 404
    
    if queried_user in matchmaking.users:
        return jsonify({"message": "Bad request, user already in matchmaking"}), 400

    with matchmaking_lock:
        matchmaking.add_user(queried_user)
        if queried_user in q:
            q.delete(queried_user)
        q.append(queried_user)

    return jsonify({"message": "Added to matchmaking queue"}), 200


@app.route("/api/v1/friendly", methods=["POST"])
def friendly():
    data = request.json
    user_name = data.get("user_name")
    opponent_name = data.get("opponent_name")


    if not user_name or not opponent_name:
        return jsonify({"message": "Missing user or opponent"}), 404


    room = str(uuid.uuid4())

    with friendly_sessions_lock:
        friendly_sessions[room] = {
            "player1": user_name,
            "player2": opponent_name
        }

    return jsonify({"message": "Game invitation created", "room": room}), 200


@socketio.on("join_friendly")
def on_join_friendly(data):
    username = data["username"]
    room = data["room"]

    with friendly_sessions_lock:
        if room not in friendly_sessions:
            emit("error", {"message": "Invalid friendly room"}, room=request.sid)
            return

        allowed_users = [friendly_sessions[room]["player1"], friendly_sessions[room]["player2"]]
        if username not in allowed_users:
            emit("error", {"message": "Unauthorized access"}, room=request.sid)
            return

    join_room(room)
    print(f"{username} has joined friendly match room {room}")

    with active_rooms_lock:
        if room not in active_rooms:
            active_rooms[room] = {}
        active_rooms[room][request.sid] = username

        current_players = list(set(active_rooms[room].values()))
        if len(current_players) == 2:
            player1 = friendly_sessions[room]["player1"]
            player2 = friendly_sessions[room]["player2"]
            symbols = {player1: "X", player2: "O"}
            emit("game_start", {"room": room, "symbols": symbols}, room=room)


@socketio.on("accept_game")
def on_accept_game(data):
    room = data["room"]
    username = data["username"]

    if room in active_rooms:
        players = list(set(active_rooms[room].values()))

        if len(players) == 2:
            with friendly_sessions_lock:
                if room not in friendly_sessions:
                    emit("error", {"message": "Invalid friendly room"}, room=room)
                    return

                player1 = friendly_sessions[room]["player1"]
                player2 = friendly_sessions[room]["player2"]

            symbols = {player1: "X", player2: "O"}
            # assing based on order, no elo to cmp

            emit("game_accepted", {"room": room, "username": username}, room=room)

            if len(active_rooms[room]) == 2:
                emit("game_start", {"room": room, "symbols": symbols}, room=room)

@socketio.on("decline_game")
def on_decline_game(data):
    room = data["room"]
    username = data["username"]

    if room in active_rooms:
        emit("game_declined", {"room": room, "username": username}, room=room)

        for sid in list(set(active_rooms[room].keys())):
            leave_room(room, sid=sid)
        del active_rooms[room]

    with friendly_sessions_lock:
        if room in friendly_sessions:
            del friendly_sessions[room]

import sys
@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]

    if room in active_rooms and username in active_rooms[room].values():
        emit("already_connected", {"room": room}, room=room)
        return # player already in room

    join_room(room)
    print(f"{username} has joined room {room}", file=sys.stderr)


    uuid1, uuid2 = uuid_from_roomname(room)

    if uuid1 == uuid2:
        emit("error", {"message": "Invalid room configuration"}, room=data["room"])
        return

    player1 = User.query.filter_by(uuid=uuid1).first()
    player2 = User.query.filter_by(uuid=uuid2).first()

    if player1.elo <= player2.elo:
        symbols = {player1.username: "X", player2.username: "O"}
    else:
        symbols = {player1.username: "O", player2.username: "X"}

    with active_rooms_lock:
        if room not in active_rooms:
            active_rooms[room] = {}
        active_rooms[room][request.sid] = username
        print("number of players in room", len(active_rooms[room]), file=sys.stderr)
        print("players in the room are:", active_rooms[room], file=sys.stderr)
        if len(set(active_rooms[room].values())) == 2: # number of unique players
            print("emitting game start", file=sys.stderr)
            emit("game_start", {"room": room, "symbols": symbols}, room=room)
        else:
            emit("already_connected", {"room": room}, room=room)

@socketio.on("connect")
def handle_connect():
    user_uuid = request.args.get("user_uuid")

    if user_uuid:
        join_room(user_uuid)
        print(f"User {user_uuid} joined their room")


@socketio.on("move")
def handle_move(data):
    """
    data:
        room (from get_room_name)
        move (x, y)
        username (str)
        symbol (X/O)

    """
    print("Received move:", data)
    room = data.get("room")
    if room:
        emit("move", data, room=room, include_self=False)


@socketio.on("disconnect")
def handle_disconnect():
    handle_disconnect_freeplay() 
    for room, players in active_rooms.items():
        if request.sid in players:
            username = players[request.sid]
            print(f"Player {username} disconnected from {room}")

            emit(
                "opponent_disconnected",
                {"message": f"{username} has disconnected"},
                room=room,
            )

            del players[request.sid]

            if not players:
                del active_rooms[room]
            break


def matchmaking_loop():
    while True:
        with matchmaking_lock:
            if len(q) < 2:
                pass

            else:
                player1 = q.popleft()
                player2 = matchmaking.find_closest_user(player1)

                if not player2:  # not enough players, wait
                    q.appendleft(player1)
                else:
                    matchmaking.remove_user(player1)
                    matchmaking.remove_user(player2)

                    if player1.uuid == player2.uuid:
                        continue

                    if player2 in q:
                        q.remove(player2)

                    room = get_room_name(player1.uuid, player2.uuid)

                    if player1.elo <= player2.elo:
                        player1_symbol, player2_symbol = "X", "O"
                    else:
                        player1_symbol, player2_symbol = "O", "X"

                    socketio.emit(
                        "match_found",
                        {"room": room, "opponent": player2.uuid, "symbol":player1_symbol},
                        room=player1.uuid,
                    )
                    socketio.emit(
                        "match_found",
                        {"room": room, "opponent": player1.uuid, "symbol": player2_symbol},
                        room=player2.uuid,
                    )

                    print(f"Matched {player1.username} vs {player2.username} in {room}")

        gevent.sleep(1)


@app.route("/api")
def hello():
    return jsonify({"organization": "Student Cyber Games"})


@app.route("/")
@app.route("/game")
@app.route("/editor")
@app.route("/editor/<string:game_uuid>")
@app.route("/game/<string:game_uuid>")
@app.route("/my-profile")
@app.route("/multiplayer")
@app.route("/multiplayer/match")
@app.route("/puzzles")
@app.route("/admin")
@app.route("/gdpr")
@app.route("/contacts")
@app.route("/register")
@app.route("/login")
def serveSPA(game_uuid=None):  # game_uuid=None parameter needed to not throw an exception
    return send_from_directory(app.static_folder, "index.html")

#Needed for flask to not throw a 404 with queryparams
@app.route('/multiplayer/friendly/')
def multiplayer():
    code = request.args.get('code')
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/v1/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        data = request.get_json()

        if not validate_game_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_game_post(data)
        if not valid_post:
            semantic_error = {"message": f"Semantic error: {message}"}
            return jsonify(semantic_error), 422

        game = Game(
            name=data["name"],
            difficulty=data["difficulty"],
            gamestate=get_gamestate(data["board"]),
            board=string_from_board(data["board"]),
            width=len(data["board"][0]),
            heigth=len(data["board"]),
        )
        db.session.add(game)
        db.session.commit()

        result = game_json(game)

        return jsonify(result), 201

    elif request.method == "GET":
        games = Game.query.all()
        return jsonify([game_json(game) for game in games]), 200


@app.route("/api/v1/games/<uuid:uuid>", methods=["GET", "PUT", "DELETE"])
def single_game(uuid):
    uuid_str = str(uuid)
    if request.method == "GET":
        game = Game.query.filter_by(uuid=uuid_str).first()
        if game is None:
            not_found = {"message": "Resource not found"}
            return jsonify(not_found), 404

        return jsonify(game_json(game)), 200

    elif request.method == "DELETE":
        game = Game.query.filter_by(uuid=uuid_str).first()

        if game is None:
            not_found = {"message": "Resource not found"}
            return jsonify(not_found), 404

        db.session.delete(game)
        db.session.commit()

        success_message = {"message": "Game deleted successfully"}
        return jsonify(success_message), 204

    elif request.method == "PUT":
        game = Game.query.filter_by(uuid=uuid_str).first()
        data = request.get_json()

        if not validate_game_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_game_post(data)
        if not valid_post:
            semantic_error = {"message": f"Semantic error: {message}"}
            return jsonify(semantic_error), 422

        game.name = data["name"]
        game.difficulty = data["difficulty"]
        game.gamestate = get_gamestate(data["board"])
        game.board = string_from_board(data["board"])
        game.updated_at = datetime.now(timezone.utc)
        game.width = len(data["board"][0])
        game.heigth = len(data["board"])

        db.session.commit()

        result = game_json(game)

        return jsonify(result), 200


@app.route("/api/v1/filter", methods=["GET"])
@app.route("/api/v1/filter/", methods=["GET"])
def filter():
    difficulty = request.args.get("difficulty", "")
    name = request.args.get("name", "")
    date_filter = request.args.get("date_filter", "")

    available_diffs = {"beginner", "easy", "medium", "hard", "extreme"}
    available_dates = {"24h", "7d", "1m", "3m"}

    difficulties = []
    if difficulty:
        difficulties = difficulty.split(",")
        if not all(diff in available_diffs for diff in difficulties):
            return (
                jsonify(
                    {
                        "message": f"Bad request: invalid difficulty, available options are {available_diffs}"
                    }
                ),
                400,
            )

    if date_filter:
        date_filters = date_filter.split(",")
        if not all(df in available_dates for df in date_filters):
            return (
                jsonify(
                    {
                        "message": f"Bad request: invalid date filter value, available options are {available_dates}"
                    }
                ),
                400,
            )

    names = []
    if name:
        names = name.split(",")

    query = Game.query

    if difficulties:
        query = query.filter(Game.difficulty.in_(difficulties))

    if name:
        query = query.filter(Game.name.in_(names))

    if date_filter:
        now = datetime.now(timezone.utc)
        date_deltas = {
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "1m": timedelta(days=30),
            "3m": timedelta(days=90),
        }

        thresholds = [
            now - date_deltas.get(df, timedelta()) for df in date_filter.split(",")
        ]
        if thresholds:
            query = query.filter(Game.updated_at >= min(thresholds))

    games = query.all()
    games_data = [
        {
            "uuid": game.uuid,
            "name": game.name,
            "gameState": game.gamestate,
            "difficulty": game.difficulty,
            "updatedAt": game.updated_at.isoformat(),
            "createdAt": game.created_at.isoformat(),
            "board": board_from_string(game.board, 15, 15),
            "width": game.width,
            "height": game.heigth,
        }
        for game in games
    ]
    return jsonify(games_data), 200


@app.route("/api/v1/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":  # synonymous with registering
        data = request.get_json()

        if not validate_user_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        if not username_is_unique(data["username"]):
            return jsonify({"message": "User with this username already exists"}), 409

        if not email_is_unique(data["email"]):
            return jsonify({"message": "User with this email already exists"}), 409

        user = User(
            username=data["username"],
            email=data["email"],
            elo=data["elo"],
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        result = user_json(user)

        return jsonify(result), 201

    elif request.method == "GET":
        users = User.query.all()
        for u in users:
            delattr(u, "password_hash")
        return jsonify([user_json(user) for user in users]), 200


@app.route("/api/v1/users/<uuid:uuid>", methods=["GET", "PUT", "DELETE"])
def single_user(uuid):
    queried_user = User.query.filter_by(uuid=str(uuid)).first()
    if not queried_user:
        return jsonify({"message": "User not found"}), 404

    if request.method == "GET":
        return jsonify(user_json(queried_user)), 200

    elif request.method == "DELETE":
        db.session.delete(queried_user)
        db.session.commit()
        return jsonify({"message": "User deleted succesfully"}), 204

    elif request.method == "PUT":
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        if not validate_user_fields(data):
            return jsonify({"message": "Bad request: missing fields"}), 400

        if username and not username_is_unique(username):
            return jsonify({"message": "User with this username already exists"}), 409

        if email and not email_is_unique(email):
            return jsonify({"message": "User with this email already exists"}), 409

        for property in data.keys():
            if property == "password":
                queried_user.set_password(data["password"])
            else:
                setattr(queried_user, property, data[property])

        db.session.commit()

        return jsonify(user_json(queried_user)), 200


@app.route("/api/v1/ban", methods=["POST"])
def ban_user():
    data = request.json
    queried_uuid = data.get("uuid")

    queried = User.query.filter_by(uuid=queried_uuid).first()

    if not queried:
        return jsonify({"error": "user not found"}), 404

    queried.is_banned = True

    db.session.commit()

    return jsonify({"message":"user succesfully banned"}), 200
    


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter((User.username == username)).first()

    if not user:
        return jsonify({"message": "Resource not found"}), 404

    if user.is_banned:
        return jsonify({"message": "user is banned"}), 403

    if not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.uuid,
        expires_delta=timedelta(hours=1),
        additional_claims={"is_admin": user.is_admin},
    )
    return jsonify({"token": access_token, "isAdmin": user.is_admin, "uuid": user.uuid})
