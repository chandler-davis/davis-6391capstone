from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment

# Register Blueprints
from app.blueprints.players import players
from app.blueprints.teams import teams
from app.blueprints.mock_drafts import mock_drafts

app.register_blueprint(players, url_prefix='/players')
app.register_blueprint(teams, url_prefix='/teams')
app.register_blueprint(mock_drafts, url_prefix='/mock-drafts')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)