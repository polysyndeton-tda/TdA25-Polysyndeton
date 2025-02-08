from src import db
from datetime import datetime, timezone
import uuid


class Game(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    name = db.Column(db.Text)
    difficulty = db.Column(db.Text)
    gamestate = db.Column(db.Text)
    board = db.Column(db.Text)
    width = db.Column(db.Integer)  # board[0] len
    heigth = db.Column(db.Integer)  # board len
