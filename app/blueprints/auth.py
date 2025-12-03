from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from app.db_connect import get_db

auth = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            # Create response with cache control headers
            response = make_response(redirect(url_for('index')))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin access required for this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        
        # Find user by username
        cursor.execute('SELECT user_id, username, email, password, role FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):
            # Login successful
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['role'] = user[4]
            
            flash(f'Welcome back, {user[1]}!', 'success')
            
            # Redirect to next page if specified, otherwise to dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    
    # Create response and add cache control headers
    response = make_response(redirect(url_for('index')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return response

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role', 'user')
        
        # Validate form data
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username or email already exists
        cursor.execute('SELECT user_id FROM users WHERE username = %s OR email = %s', (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return render_template('auth/register.html')
        
        # Hash password and create user
        hashed_password = generate_password_hash(password)
        
        try:
            cursor.execute('''INSERT INTO users (username, email, password, role) 
                             VALUES (%s, %s, %s, %s)''',
                           (username, email, hashed_password, role))
            db.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'danger')
            db.rollback()
    
    return render_template('auth/register.html')

@auth.route('/profile')
@login_required
def profile():
    """View user profile"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''SELECT user_id, username, email, role, created_at 
                     FROM users WHERE user_id = %s''', (session['user_id'],))
    user = cursor.fetchone()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.logout'))
    
    return render_template('auth/profile.html', user=user)

@auth.route('/users')
@login_required
def list_users():
    """List all users (for admins and scouts)"""
    if session.get('role') not in ['admin', 'scout']:
        flash('Access denied. Insufficient permissions.', 'danger')
        return redirect(url_for('dashboard'))
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''SELECT user_id, username, email, role, created_at 
                     FROM users ORDER BY created_at DESC''')
    users = cursor.fetchall()
    
    return render_template('auth/users.html', users=users)