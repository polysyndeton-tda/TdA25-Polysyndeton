from src.utils import string_from_board
from src.models import User


def validate_game_post(data):
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
    # je formalni chyba ulozit hru s 1 tahem (kde je jenom krizek)?
    # => mohl by to byt test edge case :D
    if set(string_from_board(data["board"])) != set([" ", "X", "O"]):
        return False, "Unsupported character"

    # Check for illegal board situations (X always starts)
    board_str = string_from_board(data["board"])
    number_of_crosses = board_str.count("X")
    number_of_noughts = board_str.count("O")
    if number_of_crosses != number_of_noughts and number_of_crosses != (
        number_of_noughts + 1
    ):
        return False, "Invalid starting player"

    return True, "OK"


def validate_game_fields(data):
    if set(list(data.keys())) != set(["name", "difficulty", "board"]):
        return False
    return True


def validate_user_fields(data):
    fields = set(["username", "email", "password", "elo"])
    if set(data.keys()) <= fields:
        return True
    return False


def username_is_unique(requested_username):
    existing_username = User.query.filter((User.username == requested_username)).first()

    if existing_username:
        return False
    return True


def email_is_unique(requested_email):
    existing_email = User.query.filter((User.email == requested_email)).first()

    if existing_email:
        return False
    return True
