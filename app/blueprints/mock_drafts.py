from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

mock_drafts = Blueprint('mock_drafts', __name__)

@mock_drafts.route('/', methods=['GET', 'POST'])
def show_mock_drafts():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new mock draft
    if request.method == 'POST':
        user_id = request.form['user_id']
        mock_name = request.form['mock_name']

        # Insert the new mock draft into the database
        cursor.execute('''INSERT INTO mock_drafts (user_id, mock_name) 
                         VALUES (%s, %s)''',
                       (user_id, mock_name))
        db.commit()

        flash('New mock draft created successfully!', 'success')
        return redirect(url_for('mock_drafts.show_mock_drafts'))

    # Handle GET request to display all mock drafts with pick counts
    cursor.execute('''
        SELECT md.mock_id, md.mock_name, md.created_at, md.updated_at,
               u.username, u.email, u.role,
               COUNT(mdp.pick_id) as pick_count
        FROM mock_drafts md
        JOIN users u ON md.user_id = u.user_id
        LEFT JOIN mock_draft_picks mdp ON md.mock_id = mdp.mock_id
        GROUP BY md.mock_id, md.mock_name, md.created_at, md.updated_at, u.username, u.email, u.role
        ORDER BY md.created_at DESC
    ''')
    all_mock_drafts = cursor.fetchall()
    
    # Get all users for dropdown
    cursor.execute('SELECT user_id, username, email, role FROM users ORDER BY username')
    all_users = cursor.fetchall()
    
    return render_template('mock_drafts.html', all_mock_drafts=all_mock_drafts, all_users=all_users)

@mock_drafts.route('/view/<int:mock_id>')
def view_mock_draft(mock_id):
    """View detailed mock draft with all picks"""
    db = get_db()
    cursor = db.cursor()

    # Get mock draft details
    cursor.execute('''
        SELECT md.mock_id, md.mock_name, md.created_at, md.updated_at,
               u.username, u.email, u.role
        FROM mock_drafts md
        JOIN users u ON md.user_id = u.user_id
        WHERE md.mock_id = %s
    ''', (mock_id,))
    
    mock_draft = cursor.fetchone()
    
    if not mock_draft:
        flash('Mock draft not found!', 'error')
        return redirect(url_for('mock_drafts.show_mock_drafts'))

    # Get all picks for this mock draft
    cursor.execute('''
        SELECT mdp.pick_id, mdp.round, mdp.pick_number,
               p.first_name, p.last_name, p.position, p.height, p.school,
               t.team_name, t.city
        FROM mock_draft_picks mdp
        JOIN players p ON mdp.player_id = p.player_id
        JOIN teams t ON mdp.target_team_id = t.team_id
        WHERE mdp.mock_id = %s
        ORDER BY mdp.round, mdp.pick_number
    ''', (mock_id,))
    
    draft_picks = cursor.fetchall()
    
    # Get available players and teams for adding picks
    cursor.execute('SELECT player_id, first_name, last_name, position, school FROM players ORDER BY last_name, first_name')
    all_players = cursor.fetchall()
    
    cursor.execute('SELECT team_id, team_name, city FROM teams ORDER BY team_name')
    all_teams = cursor.fetchall()
    
    return render_template('mock_draft_detail.html', 
                         mock_draft=mock_draft, 
                         draft_picks=draft_picks, 
                         all_players=all_players, 
                         all_teams=all_teams)

@mock_drafts.route('/add_pick/<int:mock_id>', methods=['POST'])
def add_pick(mock_id):
    """Add a pick to a mock draft"""
    db = get_db()
    cursor = db.cursor()

    player_id = request.form['player_id']
    target_team_id = request.form['target_team_id']
    round_num = request.form['round']
    pick_number = request.form['pick_number']

    # Check if pick number already exists in this mock draft
    cursor.execute('''SELECT COUNT(*) FROM mock_draft_picks 
                     WHERE mock_id = %s AND round = %s AND pick_number = %s''',
                   (mock_id, round_num, pick_number))
    
    if cursor.fetchone()[0] > 0:
        flash(f'Round {round_num}, Pick {pick_number} already exists in this mock draft!', 'warning')
        return redirect(url_for('mock_drafts.view_mock_draft', mock_id=mock_id))

    # Insert the new pick
    cursor.execute('''INSERT INTO mock_draft_picks (mock_id, player_id, round, pick_number, target_team_id) 
                     VALUES (%s, %s, %s, %s, %s)''',
                   (mock_id, player_id, round_num, pick_number, target_team_id))
    db.commit()

    flash('Pick added successfully!', 'success')
    return redirect(url_for('mock_drafts.view_mock_draft', mock_id=mock_id))

@mock_drafts.route('/update_mock_draft/<int:mock_id>', methods=['POST'])
def update_mock_draft(mock_id):
    db = get_db()
    cursor = db.cursor()

    # Update the mock draft's details
    user_id = request.form['user_id']
    mock_name = request.form['mock_name']

    cursor.execute('''UPDATE mock_drafts SET user_id = %s, mock_name = %s 
                     WHERE mock_id = %s''',
                   (user_id, mock_name, mock_id))
    db.commit()

    flash('Mock draft updated successfully!', 'success')
    return redirect(url_for('mock_drafts.show_mock_drafts'))

@mock_drafts.route('/delete_mock_draft/<int:mock_id>', methods=['POST'])
def delete_mock_draft(mock_id):
    db = get_db()
    cursor = db.cursor()

    # Delete all picks first (due to foreign key constraint)
    cursor.execute('DELETE FROM mock_draft_picks WHERE mock_id = %s', (mock_id,))
    
    # Delete the mock draft
    cursor.execute('DELETE FROM mock_drafts WHERE mock_id = %s', (mock_id,))
    db.commit()

    flash('Mock draft deleted successfully!', 'danger')
    return redirect(url_for('mock_drafts.show_mock_drafts'))

@mock_drafts.route('/delete_pick/<int:pick_id>/<int:mock_id>', methods=['POST'])
def delete_pick(pick_id, mock_id):
    """Delete a specific pick from a mock draft"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM mock_draft_picks WHERE pick_id = %s', (pick_id,))
    db.commit()

    flash('Pick deleted successfully!', 'success')
    return redirect(url_for('mock_drafts.view_mock_draft', mock_id=mock_id))

@mock_drafts.route('/api/mock_draft/<int:mock_id>')
def get_mock_draft_details(mock_id):
    """API endpoint to get mock draft details for edit modal"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT md.mock_id, md.user_id, md.mock_name,
               u.username
        FROM mock_drafts md
        JOIN users u ON md.user_id = u.user_id
        WHERE md.mock_id = %s
    ''', (mock_id,))
    
    mock_draft = cursor.fetchone()
    
    if mock_draft:
        return jsonify({
            'mock_id': mock_draft[0],
            'user_id': mock_draft[1],
            'mock_name': mock_draft[2],
            'username': mock_draft[3]
        })
    else:
        return jsonify({'error': 'Mock draft not found'}), 404

@mock_drafts.route('/api/mock_draft/<int:mock_id>/picks')
def get_mock_draft_picks(mock_id):
    """API endpoint to get picks for a mock draft"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT mdp.pick_id, mdp.round, mdp.pick_number,
               p.first_name, p.last_name, p.position,
               t.team_name, t.city
        FROM mock_draft_picks mdp
        JOIN players p ON mdp.player_id = p.player_id
        JOIN teams t ON mdp.target_team_id = t.team_id
        WHERE mdp.mock_id = %s
        ORDER BY mdp.round, mdp.pick_number
    ''', (mock_id,))
    
    picks = cursor.fetchall()
    
    return jsonify([{
        'pick_id': pick[0],
        'round': pick[1],
        'pick_number': pick[2],
        'player_name': f"{pick[3]} {pick[4]}",
        'position': pick[5],
        'team': f"{pick[6]} ({pick[7]})"
    } for pick in picks])