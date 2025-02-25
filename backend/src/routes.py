from src import app, db, socketio
from flask import jsonify, send_from_directory, request
from datetime import datetime, timezone, timedelta

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
from src.matchmaking import SortedUsers, get_room_name
from src.gamestate import get_gamestate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_socketio import emit, join_room, leave_room
from collections import deque
import gevent
from gevent.lock import BoundedSemaphore


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


matchmaking_lock = BoundedSemaphore()
matchmaking = SortedUsers()
q = deque()
active_rooms = {}


@app.route("/api/v1/matchmaking", methods=["POST"])
def matchmaking_request():
    data = request.json
    user_uuid = data.get("uuid")
    queried_user = User.query.filter_by(uuid=user_uuid).first()

    if not queried_user:
        return jsonify({"message": "User not found"}), 404

    with matchmaking_lock:
        matchmaking.add_user(queried_user)
        q.append(queried_user)

    return jsonify({"message": "Added to matchmaking queue"}), 200


@app.route("/api/v1/friendly", methods=["POST"])
def friendly():
    data = request.json
    user_username = data.get("user_username")
    opponent_username = data.get("opponent_username")

    opponent_user = User.query.filter_by(username=opponent_username).first()
    queried_user = User.query.filter_by(username=user_username).first()

    if not queried_user or not opponent_user:
        return jsonify({"message": "User not found"}), 404

    room = get_room_name(queried_user.uuid, opponent_user.uuid)

    socketio.emit(
        "game_invitation",
        {
            "room": room,
            "challenger": {
                "uuid": queried_user.uuid,
                "username": queried_user.username,
                "elo": queried_user.elo,
            },
        },
        room=opponent_user.uuid,
    )

    return jsonify({"message": "Game invitation sent", "room": room}), 200


@socketio.on("join_friendly")
def on_join_friendly(data):
    """
    data:
    username (str)
    room (str) - from get_room_name
    """
    username = data["username"]
    room = data["room"]

    join_room(room)
    print(f"{username} has joined friendly match room {room}")

    if room not in active_rooms:
        active_rooms[room] = {}
    active_rooms[room][request.sid] = username


@socketio.on("accept_game")
def on_accept_game(data):
    """
    data:
    room (str)
    username (str)
    """
    room = data["room"]
    username = data["username"]

    if room in active_rooms:
        players = list(active_rooms[room].values())

        if len(players) == 2:

            player1 = User.query.filter_by(username=players[0]).first()
            player2 = User.query.filter_by(username=players[1]).first()

            if player1.elo <= player2.elo:
                symbols = {player1.username: "X", player2.username: "O"}
            else:
                symbols = {player1.username: "O", player2.username: "X"}
            emit("game_accepted", {"room": room, "username": username}, room=room)

            if len(active_rooms[room]) == 2:
                emit("game_start", {"room": room, "symbols":symbols}, room=room)


@socketio.on("decline_game")
def on_decline_game(data):
    """
    data:
    room (str)
    username (str)
    """
    room = data["room"]
    username = data["username"]

    if room in active_rooms:
        emit("game_declined", {"room": room, "username": username}, room=room)

        for sid in list(active_rooms[room].keys()):
            leave_room(room, sid=sid)
        del active_rooms[room]


@socketio.on("join")
def on_join(data):
    """
    data:
        username (str)
        room (from get_room_name)
    """
    username = data["username"]
    room = data["room"]
    join_room(room)
    print(f"{username} has joined room {room}")

    if room not in active_rooms:
        active_rooms[room] = {}
    active_rooms[room][request.sid] = username

    if room in active_rooms and len(active_rooms[room]) == 2:
        emit("game_start", {"room": room}, room=room)


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

                    if player2 in q:
                        q.remove(player2)

                    room = get_room_name(player1.uuid, player2.uuid)
                    active_rooms[room] = {player1.uuid, player2.uuid}

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
@app.route("/multiplayer/friendly")
@app.route("/puzzles")
@app.route("/admin")
@app.route("/gdpr")
@app.route("/contacts")
def serveSPA(game_uuid=None):  # game_uuid=None parameter needed to not throw an exception
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


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter((User.username == username)).first()

    if not user:
        return jsonify({"message": "Resource not found"}), 404

    if not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.uuid,
        expires_delta=timedelta(hours=1),
        additional_claims={"is_admin": user.is_admin},
    )
    return jsonify({"token": access_token, "isAdmin": user.is_admin, "uuid": user.uuid})
