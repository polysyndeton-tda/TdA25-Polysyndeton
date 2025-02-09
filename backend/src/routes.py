from src import app, db
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
)
from src.gamestate import get_gamestate


@app.route("/api")
def hello():
    return jsonify({"organization": "Student Cyber Games"})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/game")
@app.route("/editor")
@app.route("/editor/<string:game_uuid>")
@app.route("/game/<string:game_uuid>")
def serve_game(game_uuid=None):
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
        # query = query.filter(Game.name.ilike(f"%{name}%"))  # Case-insensitive partial match
        query = query.filter(Game.name.in_(names))

    if date_filter:
        now = datetime.now(timezone.utc)
        date_deltas = {
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "1m": timedelta(days=30),
            "3m": timedelta(days=90)
        }
    
        thresholds = [now - date_deltas.get(df, timedelta()) for df in date_filter.split(",")]
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
    if request.method == "POST":
        data = request.get_json()

        if not validate_user_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        user = User(
            username=data["username"],
            email=data["email"],
            elo=data["elo"],
            # password?
        )
        db.session.add(user)
        db.session.commit()

        result = user_json(user)

        return jsonify(result), 201

    elif request.method == "GET":
        users = User.query.all()
        return jsonify([user_json(user) for user in users]), 200


@app.route("/api/v1/user/<uuid:uuid>", methods=["GET", "PUT", "DELETE"])
def user(uuid):
    uuid_str = str(uuid)

    if request.method == "GET":
        user = User.query.filter_by(uuid=uuid_str).first()
        if user is None:
            not_found = {"message": "Resource not found"}
            return jsonify(not_found), 404

        return jsonify(game_json(user)), 200

    elif request.method == "DELETE":
        user = User.query.filter_by(uuid=uuid_str).first()

        if user is None:
            not_found = {"message": "Resource not found"}
            return jsonify(not_found), 404

        db.session.delete(user)
        db.session.commit()

        success_message = {"message": "User deleted successfully"}
        return jsonify(success_message), 204

    elif request.method == "PUT":
        user = User.query.filter_by(uuid=uuid_str).first()
        data = request.get_json()

        if not validate_user_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        user.username = data["username"]
        user.email = data["email"]
        user.password = data["password"]
        user.elo = data["elo"]
        db.session.commit()

        result = user_json(user)

        return jsonify(result), 200
