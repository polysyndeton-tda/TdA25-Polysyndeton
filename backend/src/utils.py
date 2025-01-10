from datetime import datetime, timezone

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
    #je formalni chyba ulozit hru s 1 tahem (kde je jenom krizek)?
    # => mohl by to byt test edge case :D
    if set(string_from_board(data["board"])) != set([" ", "X", "O"]):
        return False, "Unsupported character"
    
    #Check for illegal board situations (X always starts)
    board_str = string_from_board(data["board"])
    number_of_crosses = board_str.count("X")
    number_of_noughts = board_str.count("O")
    if number_of_crosses != number_of_noughts and number_of_crosses != (number_of_noughts + 1):
        return False, "Invalid starting player"

    return True, "OK"


def validate_fields(data):
    if set(list(data.keys())) != set(["name", "difficulty", "board"]):
        return False
    return True


def get_gamestate(board):
    pass
