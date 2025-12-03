from flask import render_template, session, redirect, url_for
from . import app
from app.blueprints.auth import login_required

@app.route('/')
def index():
    # If user is logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')
