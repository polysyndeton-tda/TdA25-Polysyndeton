from werkzeug.security import generate_password_hash
from src.models import User, db
from config import Config

def init_admin():
    admin = User.query.filter_by(username=Config.SUPERUSER_USERNAME).first()
    if not admin:
        admin = User(
            username=Config.SUPERUSER_USERNAME,
            email=Config.SUPERUSER_EMAIL,
            is_admin=True
        )
        admin.set_password(Config.SUPERUSER_PASSWORD)
        db.session.add(admin)
        db.session.commit()