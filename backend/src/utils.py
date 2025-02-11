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


def user_json(user):
    result = {
        "uuid": user.uuid,
        "createdAt": get_formatted_date(user.updated_at),
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "elo": user.elo,
        "wins": user.wins,
        "losses": user.draws,
        "draws": user.draws,
    }

    return result
