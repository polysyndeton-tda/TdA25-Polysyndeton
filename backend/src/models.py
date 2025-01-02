from src import db
from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property

class Game(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    name = db.Column(db.Text)
    difficulty = db.Column(db.Text)
    gamestate = db.Column(db.Text)
    board = db.Column(db.Text)

    @hybrid_property
    def created_at(self):
        if self.created_at:
            return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' if self.created_at else None

    @hybrid_property
    def updated_at(self):
        if self.created_at:
            return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' if self.created_at else None