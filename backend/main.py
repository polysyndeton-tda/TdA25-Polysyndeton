import sqlalchemy as sa
import sqlalchemy.orm as so
from src import app, db
from src.models import Game

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, host="0.0.0.0", port=5000)


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so, "db": db, "Game": Game}
