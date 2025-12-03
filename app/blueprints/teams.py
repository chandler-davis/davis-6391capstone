from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db
from app.blueprints.auth import login_required

teams = Blueprint('teams', __name__)

@teams.route('/', methods=['GET', 'POST'])
@login_required
def show_teams():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new team
    if request.method == 'POST':
        team_name = request.form['team_name']
        city = request.form['city']
        conference = request.form['conference']

        # Insert the new team into the database
        cursor.execute('''INSERT INTO teams (team_name, city, conference) 
                         VALUES (%s, %s, %s)''',
                       (team_name, city, conference))
        db.commit()

        flash('New team added successfully!', 'success')
        return redirect(url_for('teams.show_teams'))

    # Handle GET request to display all teams with player count
    cursor.execute('''
        SELECT t.team_id, t.team_name, t.city, t.conference, t.created_at, t.updated_at,
               COUNT(p.player_id) as player_count
        FROM teams t
        LEFT JOIN players p ON t.team_id = p.primary_team_id
        GROUP BY t.team_id, t.team_name, t.city, t.conference, t.created_at, t.updated_at
        ORDER BY t.conference, t.team_name
    ''')
    all_teams = cursor.fetchall()
    
    return render_template('teams.html', all_teams=all_teams)

@teams.route('/update_team/<int:team_id>', methods=['POST'])
@login_required
def update_team(team_id):
    db = get_db()
    cursor = db.cursor()

    # Update the team's details
    team_name = request.form['team_name']
    city = request.form['city']
    conference = request.form['conference']

    cursor.execute('''UPDATE teams SET team_name = %s, city = %s, conference = %s 
                     WHERE team_id = %s''',
                   (team_name, city, conference, team_id))
    db.commit()

    flash('Team updated successfully!', 'success')
    return redirect(url_for('teams.show_teams'))

@teams.route('/delete_team/<int:team_id>', methods=['POST'])
@login_required
def delete_team(team_id):
    db = get_db()
    cursor = db.cursor()

    # Check if team has players assigned to it
    cursor.execute('SELECT COUNT(*) FROM players WHERE primary_team_id = %s', (team_id,))
    player_count = cursor.fetchone()[0]
    
    if player_count > 0:
        flash(f'Cannot delete team. {player_count} player(s) are assigned to this team. Please reassign players first.', 'warning')
        return redirect(url_for('teams.show_teams'))

    # Delete the team
    cursor.execute('DELETE FROM teams WHERE team_id = %s', (team_id,))
    db.commit()

    flash('Team deleted successfully!', 'danger')
    return redirect(url_for('teams.show_teams'))

@teams.route('/api/team/<int:team_id>')
@login_required
def get_team_details(team_id):
    """API endpoint to get team details for edit modal"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT team_id, team_name, city, conference
        FROM teams
        WHERE team_id = %s
    ''', (team_id,))
    
    team = cursor.fetchone()
    
    if team:
        return jsonify({
            'team_id': team[0],
            'team_name': team[1],
            'city': team[2],
            'conference': team[3]
        })
    else:
        return jsonify({'error': 'Team not found'}), 404

@teams.route('/api/team/<int:team_id>/players')
@login_required
def get_team_players(team_id):
    """API endpoint to get players assigned to a team"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT player_id, first_name, last_name, position
        FROM players
        WHERE primary_team_id = %s
        ORDER BY last_name, first_name
    ''', (team_id,))
    
    players = cursor.fetchall()
    
    return jsonify([{
        'player_id': player[0],
        'first_name': player[1],
        'last_name': player[2],
        'position': player[3]
    } for player in players])