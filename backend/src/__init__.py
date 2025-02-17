import logging
import os

from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# outside Docker, this folder ../../frontend/build works as static folder
# however inside Docker, that relative link does not work, the directory layout is different (the build folder is still present in the Docker image though)
# so it doesn't find the build folder
# => so changing it back to ../static, which is reachable in both cases
# however for builds outside of docker this means that the build folder has to be copied to the static folder
# => updated build.sh to copy the build folder to the static folder
app = Flask(__name__, static_folder="../static")  # ../../frontend/build
app.config.from_object(Config)

for k in os.environ.keys():
    logger.info(f"Available environment variable: {k}")

jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src import routes
