import logging
import os

from flask import Flask
from logging.handlers import RotatingFileHandler

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

# outside Docker, this folder ../../frontend/build works as static folder
# however inside Docker, that relative link does not work, the directory layout is different (the build folder is still present in the Docker image though)
# so it doesn't find the build folder
# => so changing it back to ../static, which is reachable in both cases
# however for builds outside of docker this means that the build folder has to be copied to the static folder
# => updated build.sh to copy the build folder to the static folder
app = Flask(__name__, static_folder="../static")  # ../../frontend/build
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src import routes

if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/ports.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Ports game")
