from src.models import User
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
        candidates = []

        if idx > 0:
            candidates.append(self.users[idx - 1])

        if idx < len(self.users):
            candidates.append(self.users[idx + 1])

        candidates = [candidate for candidate in candidates if candidate != user]

        if not candidates:
            return None

        closest = min(candidates, key=lambda candidate: abs(candidate.elo - user.elo))
        return closest


def get_room_name(uuid1, uuid2):
    sorted_uuids = sorted([uuid1, uuid2])
    return f"room_{sorted_uuids[0]}_{sorted_uuids[1]}"
