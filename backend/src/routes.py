from src import app, db
from flask import jsonify, send_from_directory, request

from src.models import Game

@app.route('/api')
def hello():
    return jsonify({"organization": "Student Cyber Games"})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.static_folder, path)

@app.route('/games', methods=["GET", "POST"])
def games():
    data = request.get_json()
    if request.method == "POST":
        game = Game()
        return jsonify({"uuid": game.uuid})

    elif request.method == "GET":
        pass
