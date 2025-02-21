from src.models import User
from src import db
import uuid

def get_game_users():
    user1 = User(
        username="user1",
        email="1a.com",
        elo=400,
    )
    user1.set_password("blbl")

    user2 = User(
        username="user2",
        email="2a.com",
        elo=400,
    )
    user2.set_password("blbl")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    return user1, user2

def get_room_name(uuid1, uuid2):
    sorted_ids = sorted([uuid1, uuid2])
    return f"room_{sorted_ids[0]}_{sorted_ids[1]}"