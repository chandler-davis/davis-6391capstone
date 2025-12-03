from flask import Flask, g, session, make_response
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment

# Register Blueprints
from app.blueprints.auth import auth
from app.blueprints.players import players
from app.blueprints.teams import teams
from app.blueprints.mock_drafts import mock_drafts
from app.blueprints.stats import stats

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(players, url_prefix='/players')
app.register_blueprint(teams, url_prefix='/teams')
app.register_blueprint(mock_drafts, url_prefix='/mock-drafts')
app.register_blueprint(stats, url_prefix='/stats')

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

# Add cache control headers to prevent back button access after logout
@app.after_request
def add_cache_control_headers(response):
    """Add cache control headers to prevent caching of protected pages"""
    if 'user_id' in session:
        # For logged-in users, set headers to prevent caching of protected pages
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Enhanced session security
@app.before_request
def check_session_validity():
    """Check if session is valid and clear expired sessions"""
    from flask import request
    
    # Allow access to public routes without session check
    public_routes = ['auth.login', 'auth.register', 'auth.logout', 'index', 'static']
    if request.endpoint in public_routes:
        return
    
    # For protected routes, ensure session is valid
    if 'user_id' in session:
        # Verify user still exists in database (optional security check)
        try:
            db = get_db()
            if db:
                cursor = db.cursor()
                cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (session['user_id'],))
                if not cursor.fetchone():
                    # User no longer exists, clear session
                    session.clear()
        except:
            # Database error, continue normally
            pass