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
    JWT_SECRET_KEY = os.environ["SECRET_KEY"] or os.environ["JWT_SECRET_KEY"]

    logger.info("Listing all environment variables:")
    for key, value in os.environ.items():
        logger.info(f"{key}: {value}")
