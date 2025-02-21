from src.models import User
from src import db
import uuid
from sortedcontainers import SortedList

class SortedUsers:
    def __init__(self):
        self.users = SortedList(key=lambda user: user.elo)

    def add_user(self, user: User):
        self.users.add(user)

    def remove_user(self, user: User):
        self.users.remove(user)

    def find_closest_user(self, user: User):
        if not self.users:
            return None
        
        idx = self.users.bisect_left(user)
        closest = None

        if idx > 0:
            closest = self.users[idx - 1]
        
        if idx < len(self.users):
            if closest is None or abs(self.users[idx].elo - user.elo) < abs(closest.elo - user.elo):
                closest = self.users[idx]

        return closest

def get_room_name(uuid1, uuid2):
    sorted_uuids = sorted([uuid1, uuid2])
    return f"room_{sorted_uuids[0]}_{sorted_uuids[1]}"