from src import db
from datetime import datetime, timezone
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Boolean


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


class User(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    elo = db.Column(db.Integer, nullable=False, default=400)
    wins = db.Column(db.Integer, nullable=False, default=0)
    draws = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(Boolean, default=False)
    is_banned = db.Column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def create_superuser():
    from config import Config

    superuser = User.query.filter_by(username=Config.SUPERUSER_USERNAME).first()
    if not superuser:
        superuser = User(
            username=Config.SUPERUSER_USERNAME,
            email=Config.SUPERUSER_EMAIL,
            is_admin=True,
        )
        superuser.set_password(Config.SUPERUSER_PASSWORD)
        db.session.add(superuser)
        db.session.commit()
