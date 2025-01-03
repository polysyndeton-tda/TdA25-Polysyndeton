from src import app, db
from flask import jsonify, send_from_directory, request, Response
import json
from datetime import datetime, timezone

from src.models import Game
from src.utils import (
    string_from_board,
    game_json,
    validate_post,
    validate_fields,
    get_gamestate,
    get_formatted_date,
)


@app.route("/api")
def hello():
    return jsonify({"organization": "Student Cyber Games"})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/v1/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        data = request.get_json()

        if not validate_fields(data):
            bad_request = {"code": 400, "message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_post(data)
        if not valid_post:
            semantic_error = {"code": 422, "message": f"Semantic error: {message}"}
            return jsonify(semantic_error), 404

        game = Game(
            name=data["name"],
            difficulty=data["difficulty"],
            gamestate="unknown",
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
            not_found = {"code": 404, "message": "Resource not found"}
            return jsonify(not_found), 404

        return jsonify(game_json(game)), 200

    elif request.method == "DELETE":
        game = Game.query.filter_by(uuid=uuid_str).first()

        if game is None:
            not_found = {"code": 404, "message": "Resource not found"}
            return jsonify(not_found), 404

        db.session.delete(game)
        db.session.commit()

        success_message = {"code": 200, "message": "Game deleted successfully"}
        return jsonify(success_message), 200

    elif request.method == "PUT":
        game = Game.query.filter_by(uuid=uuid_str).first()
        data = request.get_json()

        if not validate_fields(data):
            bad_request = {"code": 400, "message": "Bad request: missing fields"}
            return jsonify(bad_request), 400

        valid_post, message = validate_post(data)
        if not valid_post:
            semantic_error = {"code": 422, "message": f"Semantic error: {message}"}
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
