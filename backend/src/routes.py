from src import app, db
from flask import jsonify, send_from_directory, request, Response
import json

from src.models import Game
from src.utils import string_from_board, game_json, validate_post, validate_fields


@app.route("/api")
def hello():
    return jsonify({"organization": "Student Cyber Games"})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve(path):
    return send_from_directory(app.static_folder, path)


@app.route("/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        data = request.get_json()

        if not validate_fields(data):
            bad_request = {"code": 400, "message": "Bad request: missing fields"}
            return Response(json.dumps(bad_request), status=400)

        valid_post, message = validate_post(data)
        if not valid_post:
            semantic_error = {"code": 422, "message": f"Semantic error: {message}"}
            return Response(json.dumps(semantic_error), status=422)

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

        return Response(
            json.dumps(result, ensure_ascii=False),
            status=201,
            content_type="application/json; charset=utf-8",
        )

    elif request.method == "GET":
        games = Game.query.all()

        return Response(
            json.dumps([game_json(game) for game in games]),
            status=200,
            content_type="application/json; charset=utf-8",
        )


@app.route("/games/<uuid:uuid>", methods=["GET", "PUT", "DELETE"])
def single_game(uuid):
    uuid_str = str(uuid)
    if request.method == "GET":
        game = Game.query.filter_by(uuid=uuid_str).first()
        if game is None:
            not_found = {"code": 404, "message": "Resource not found"}
            return Response(
                json.dumps(not_found),
                status=404,
            )

        return Response(
            json.dumps(game_json(game)),
            status=200,
        )
