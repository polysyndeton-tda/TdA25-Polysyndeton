from src import app, db
from flask import jsonify, send_from_directory, request, Response
import json

from src.models import Game
from src.utils import string_from_board, board_from_string, get_formatted_date


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

        result = {
            "uuid": game.uuid,
            "createdAt": get_formatted_date(game.created_at),
            "updatedAt": get_formatted_date(game.updated_at),
            "name": game.name,
            "difficulty": game.difficulty,
            "gameState": game.gamestate,
            "board": board_from_string(game.board, game.heigth, game.width),
        }

        return Response(
            json.dumps(result, ensure_ascii=False),
            status=201,
            content_type="application/json; charset=utf-8",
        )

    elif request.method == "GET":
        pass
