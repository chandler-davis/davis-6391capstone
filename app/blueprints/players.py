from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

players = Blueprint('players', __name__)

@players.route('/', methods=['GET', 'POST'])
def show_players():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new player
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        height = request.form['height']
        school = request.form['school']
        age = request.form['age']
        primary_team_id = request.form['primary_team_id'] if request.form['primary_team_id'] else None

        # Insert the new player into the database
        cursor.execute('''INSERT INTO players (first_name, last_name, position, height, school, age, primary_team_id) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (first_name, last_name, position, height, school, age, primary_team_id))
        db.commit()

        flash('New player added successfully!', 'success')
        return redirect(url_for('players.show_players'))

    # Handle GET request to display all players with team information
    cursor.execute('''
        SELECT p.player_id, p.first_name, p.last_name, p.position, p.height, 
               p.school, p.age, p.primary_team_id, p.created_at, p.updated_at,
               t.team_name, t.city
        FROM players p
        LEFT JOIN teams t ON p.primary_team_id = t.team_id
        ORDER BY p.last_name, p.first_name
    ''')
    all_players = cursor.fetchall()
    
    # Get all teams for dropdown
    cursor.execute('SELECT team_id, team_name, city FROM teams ORDER BY team_name')
    all_teams = cursor.fetchall()
    
    return render_template('players.html', all_players=all_players, all_teams=all_teams)

@players.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Update the player's details
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    position = request.form['position']
    height = request.form['height']
    school = request.form['school']
    age = request.form['age']
    primary_team_id = request.form['primary_team_id'] if request.form['primary_team_id'] else None

    cursor.execute('''UPDATE players SET first_name = %s, last_name = %s, position = %s, 
                     height = %s, school = %s, age = %s, primary_team_id = %s 
                     WHERE player_id = %s''',
                   (first_name, last_name, position, height, school, age, primary_team_id, player_id))
    db.commit()

    flash('Player updated successfully!', 'success')
    return redirect(url_for('players.show_players'))

@players.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the player
    cursor.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
    db.commit()

    flash('Player deleted successfully!', 'danger')
    return redirect(url_for('players.show_players'))

@players.route('/api/player/<int:player_id>')
def get_player_details(player_id):
    """API endpoint to get player details for edit modal"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT p.player_id, p.first_name, p.last_name, p.position, p.height, 
               p.school, p.age, p.primary_team_id,
               t.team_name, t.city
        FROM players p
        LEFT JOIN teams t ON p.primary_team_id = t.team_id
        WHERE p.player_id = %s
    ''', (player_id,))
    
    player = cursor.fetchone()
    
    if player:
        return jsonify({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'position': player[3],
            'height': player[4],
            'school': player[5],
            'age': player[6],
            'primary_team_id': player[7],
            'team_name': player[8],
            'city': player[9]
        })
    else:
        return jsonify({'error': 'Player not found'}), 404