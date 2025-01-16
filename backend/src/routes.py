from src import app, db
from flask import jsonify, send_from_directory, request, Response
import json
from datetime import datetime, timezone, timedelta

from src.models import Game
from src.utils import (
    string_from_board,
    game_json,
    validate_post,
    validate_fields,
    get_gamestate,
    get_formatted_date,
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

        if not validate_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_post(data)
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

        if not validate_fields(data):
            bad_request = {"message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_post(data)
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

@app.route("/api/v1/filter/")
def filter():
    difficulty = request.args.get("difficulty")
    name = request.args.get("name")
    date_filter = request.args.get("date_filter") 

    available_diffs = {"beginner", "easy", "medium", "hard", "extreme"}
    if difficulty not in available_diffs:
        bad_request = {"message": f"Bad request: invalid difficulty, available options are {available_diffs}"}
        return jsonify(bad_request), 400

    query = Game.query

    if difficulty:
        query = query.filter(Game.difficulty == difficulty)

    if name:
        query = query.filter(Game.name.ilike(f"%{name}%")) # case insensitive

    available_dates = {"24h", "7d", "1m", "3m"}
    if date_filter:
        now = datetime.now(timezone.utc)
        if date_filter == "24h":
            threshold = now - timedelta(hours=24)
        elif date_filter == "7d":
            threshold = now - timedelta(days=7)
        elif date_filter == "1m":
            threshold = now - timedelta(days=30)
        elif date_filter == "3m":
            threshold = now - timedelta(days=90)
        else:
            return jsonify({"Bad request": f"invalid date filter value, available options are: {available_dates}"}), 400

        query = query.filter(Game.updated_at >= threshold)

    games = query.all()

    games_data = [
        {
            "uuid": game.uuid,
            "name": game.name,
            "difficulty": game.difficulty,
            "updated_at": game.updated_at.isoformat(),
            "created_at": game.created_at.isoformat(),
            "board": game.board,
            "width": game.width,
            "height": game.heigth,
        }
        for game in games
    ]

    return jsonify(games_data), 200