import os
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger(__name__)


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "secret-key"
    SECRET_KEY = os.getenv("SECRET_KEY") or "secret-key"
    SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL") or "tda@scg.cz"
    SUPERUSER_USERNAME = os.getenv("SUPERUSER_USERNAME") or "TdA"
    SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD") or "StudentCyberGames25!"

    logger.info("Listing all environment variables:")
    for key, value in os.environ.items():
        logger.info(f"{key}: {value}")
