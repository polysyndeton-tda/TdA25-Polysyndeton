from datetime import datetime, timezone
import sys

def get_formatted_date(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def string_from_board(board):
    return "".join(
        ["".join([point if point != "" else " " for point in row]) for row in board]
    )


def board_from_string(string, heigth, width):
    board = [list(string[(i) * width : (i + 1) * width]) for i in range(heigth)]
    board = [[i if i != " " else "" for i in row] for row in board]
    return board


def game_json(game):
    result = {
        "uuid": game.uuid,
        "createdAt": get_formatted_date(game.created_at),
        "updatedAt": get_formatted_date(game.updated_at),
        "name": game.name,
        "difficulty": game.difficulty,
        "gameState": game.gamestate,
        "board": board_from_string(game.board, game.heigth, game.width),
    }

    return result


def validate_post(data):
    diffs = {"beginner", "easy", "medium", "hard", "extreme"}
    if data["difficulty"] not in diffs:
        return False, "Unsupported difficulty"

    REQUIRED_LENGTH = 15
    for row in data["board"]:
        if len(row) != REQUIRED_LENGTH:
            return False, "Invalid row length"

    TOTAL_SIZE = 225
    if len(string_from_board(data["board"])) != TOTAL_SIZE:
        return False, "Invalid board size"
    print(set(string_from_board(data["board"])), file=sys.stderr)
    #je formalni chyba ulozit hru s 1 tahem (kde je jenom krizek)?
    # => mohl by to byt test edge case :D
    if set(string_from_board(data["board"])) != set([" ", "X", "O"]):
        return False, "Unsupported character"

    return True, "OK"


def validate_fields(data):
    print(list(data.keys()), file=sys.stderr)
    #validate_fields je spolecna funkce pro oba routy, takze musi podporovat oba pripady
    # NN, v obou případech je nutné mít name, difficulty, board (A ZBYTEK NENÍ)
    #=> STEJNĚ SE VĚCI JAKO UPDATED A UUID DOGENERUJÍ NA SERVERU
    #pro /games POST, kde nutny je jenom name, difficulty, board
    #pro /games/uuid PUT, kde uz to ma z serveru i dalsi veci jako ['board', 'createdAt', 'difficulty', 'gameState', 'name', 'updatedAt', 'uuid']
    if set(list(data.keys())) != set(["name", "difficulty", "board", "uuid"]): #for the games route, you need to support uuid, see: https://odevzdavani.tourdeapp.cz/mockbush/swagger#tag/default/POST/api/v1/games/
        return False
    return True


def get_gamestate(board):
    pass
