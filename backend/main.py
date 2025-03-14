import sqlalchemy as sa
import sqlalchemy.orm as so
from src import app, db, socketio
from src.models import Game
import gevent
from src.routes import matchmaking_loop
from werkzeug.debug import DebuggedApplication

if __name__ == "__main__":
    print(app.url_map)

    gevent.spawn(matchmaking_loop)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)

    #if app.debug is set to true, allow us to see the Flask Debugger through Web UI (requires entering Flask Debugger-PIN)
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so, "db": db, "Game": Game}
