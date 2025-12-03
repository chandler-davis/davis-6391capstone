from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db
from app.blueprints.auth import login_required

players = Blueprint('players', __name__)

@players.route('/', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the player
    cursor.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
    db.commit()

    flash('Player deleted successfully!', 'danger')
    return redirect(url_for('players.show_players'))

@players.route('/api/player/<int:player_id>')
@login_required
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

@players.route('/update_to_current/<int:player_id>', methods=['POST'])
@login_required
def update_to_current(player_id):
    """Update player information to current 2024-25 season data"""
    db = get_db()
    cursor = db.cursor()
    
    # Get current player info
    cursor.execute('SELECT first_name, last_name FROM players WHERE player_id = %s', (player_id,))
    player = cursor.fetchone()
    
    if not player:
        return jsonify({'success': False, 'message': 'Player not found'}), 404
    
    first_name, last_name = player[0], player[1]
    player_full_name = f"{first_name} {last_name}"
    
    # Current 2025-26 season data for our prospects
    current_data = {
        'JuJu Watkins': {'school': 'USC', 'age': 20, 'height': '6\'2\"', 'position': 'SG'},
        'Hannah Hidalgo': {'school': 'Notre Dame', 'age': 20, 'height': '5\'6\"', 'position': 'PG'},
        'Flau\'jae Johnson': {'school': 'LSU', 'age': 22, 'height': '5\'10\"', 'position': 'SG'},
        'Raven Johnson': {'school': 'South Carolina', 'age': 22, 'height': '5\'8\"', 'position': 'PG'},
        'Shyanne Sellers': {'school': 'South Carolina', 'age': 22, 'height': '5\'11\"', 'position': 'SF'},
        'Kaitlyn Chen': {'school': 'Princeton', 'age': 23, 'height': '5\'9\"', 'position': 'PG'},
        'Madison Booker': {'school': 'Texas', 'age': 23, 'height': '5\'9\"', 'position': 'SG'},
        'Azzi Fudd': {'school': 'UConn', 'age': 22, 'height': '5\'11\"', 'position': 'SG'},
        'Olivia Miles': {'school': 'TCU', 'age': 22, 'height': '5\'10\"', 'position': 'PG'},
        'Lauren Betts': {'school': 'UCLA', 'age': 21, 'height': '6\'7\"', 'position': 'C'},
        'Janiah Barker': {'school': 'UCLA', 'age': 22, 'height': '5\'10\"', 'position': 'SF'},
        'Mila Reynolds': {'school': 'Utah', 'age': 23, 'height': '6\'1\"', 'position': 'SF'},
        'Timea Gardiner': {'school': 'Oregon State', 'age': 23, 'height': '6\'3\"', 'position': 'C'},
        'Leigha Brown': {'school': 'Michigan', 'age': 23, 'height': '5\'9\"', 'position': 'SG'},
        'Saniya Rivers': {'school': 'NC State', 'age': 21, 'height': '5\'8\"', 'position': 'PG'},
        'Cotie McMahon': {'school': 'Ole Miss', 'age': 21, 'height': '5\'9\"', 'position': 'SF'}
    }
    
    if player_full_name in current_data:
        data = current_data[player_full_name]
        try:
            cursor.execute('''UPDATE players 
                             SET school = %s, age = %s, height = %s, position = %s 
                             WHERE player_id = %s''',
                           (data['school'], data['age'], data['height'], data['position'], player_id))
            db.commit()
            
            return jsonify({
                'success': True, 
                'message': f'Updated {player_full_name} with current 2025-26 season information',
                'updated_data': data
            })
        except Exception as e:
            db.rollback()
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    else:
        return jsonify({
            'success': False, 
            'message': f'No current data available for {player_full_name}. Please update manually.'
        }), 404

@players.route('/update_all_to_current', methods=['POST'])
@login_required
def update_all_to_current():
    """Update all players' information to current 2024-25 season data"""
    db = get_db()
    cursor = db.cursor()
    
    # Current 2025-26 season data for our prospects
    current_data = {
        'JuJu Watkins': {'school': 'USC', 'age': 20, 'height': '6\'2\"', 'position': 'SG'},
        'Hannah Hidalgo': {'school': 'Notre Dame', 'age': 20, 'height': '5\'6\"', 'position': 'PG'},
        'Flau\'jae Johnson': {'school': 'LSU', 'age': 22, 'height': '5\'10\"', 'position': 'SG'},
        'Raven Johnson': {'school': 'South Carolina', 'age': 22, 'height': '5\'8\"', 'position': 'PG'},
        'Shyanne Sellers': {'school': 'South Carolina', 'age': 22, 'height': '5\'11\"', 'position': 'SF'},
        'Kaitlyn Chen': {'school': 'Princeton', 'age': 23, 'height': '5\'9\"', 'position': 'PG'},
        'Madison Booker': {'school': 'Texas', 'age': 23, 'height': '5\'9\"', 'position': 'SG'},
        'Azzi Fudd': {'school': 'UConn', 'age': 22, 'height': '5\'11\"', 'position': 'SG'},
        'Olivia Miles': {'school': 'TCU', 'age': 22, 'height': '5\'10\"', 'position': 'PG'},
        'Lauren Betts': {'school': 'UCLA', 'age': 21, 'height': '6\'7\"', 'position': 'C'},
        'Janiah Barker': {'school': 'UCLA', 'age': 22, 'height': '5\'10\"', 'position': 'SF'},
        'Mila Reynolds': {'school': 'Utah', 'age': 23, 'height': '6\'1\"', 'position': 'SF'},
        'Timea Gardiner': {'school': 'Oregon State', 'age': 23, 'height': '6\'3\"', 'position': 'C'},
        'Leigha Brown': {'school': 'Michigan', 'age': 23, 'height': '5\'9\"', 'position': 'SG'},
        'Saniya Rivers': {'school': 'NC State', 'age': 21, 'height': '5\'8\"', 'position': 'PG'},
        'Cotie McMahon': {'school': 'Ole Miss', 'age': 21, 'height': '5\'9\"', 'position': 'SF'}
    }
    
    # Get all players
    cursor.execute('SELECT player_id, first_name, last_name FROM players')
    all_players = cursor.fetchall()
    
    updated_count = 0
    errors = []
    
    try:
        for player in all_players:
            player_id, first_name, last_name = player[0], player[1], player[2]
            player_full_name = f"{first_name} {last_name}"
            
            if player_full_name in current_data:
                data = current_data[player_full_name]
                try:
                    cursor.execute('''UPDATE players 
                                     SET school = %s, age = %s, height = %s, position = %s 
                                     WHERE player_id = %s''',
                                   (data['school'], data['age'], data['height'], data['position'], player_id))
                    updated_count += 1
                except Exception as e:
                    errors.append(f"Error updating {player_full_name}: {str(e)}")
        
        if errors:
            db.rollback()
            return jsonify({
                'success': False, 
                'message': f'Some updates failed: {"; ".join(errors)}'
            }), 500
        else:
            db.commit()
            return jsonify({
                'success': True,
                'message': f'Successfully updated {updated_count} players',
                'updated_count': updated_count
            })
            
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

@players.route('/info/<int:player_id>')
@login_required  
def get_player_info(player_id):
    """Get comprehensive player information including stats for info modal"""
    db = get_db()
    cursor = db.cursor()
    
    # Get player basic info
    cursor.execute('''
        SELECT p.player_id, p.first_name, p.last_name, p.position, p.height, 
               p.school, p.age, p.primary_team_id, p.created_at, p.updated_at,
               t.team_name, t.city
        FROM players p
        LEFT JOIN teams t ON p.primary_team_id = t.team_id
        WHERE p.player_id = %s
    ''', (player_id,))
    
    player = cursor.fetchone()
    
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    
    # Get player stats
    cursor.execute('''
        SELECT season, games_played, ppg, rpg, apg, fg_pct, three_pt_pct
        FROM player_stats 
        WHERE player_id = %s 
        ORDER BY season DESC
        LIMIT 1
    ''', (player_id,))
    
    stats = cursor.fetchone()
    
    # Build response
    player_info = {
        'player_id': player[0],
        'first_name': player[1], 
        'last_name': player[2],
        'position': player[3],
        'height': player[4],
        'school': player[5],
        'age': player[6],
        'primary_team_id': player[7],
        'created_at': player[8].strftime('%Y-%m-%d') if player[8] else None,
        'updated_at': player[9].strftime('%Y-%m-%d') if player[9] else None,
        'team_name': player[10],
        'city': player[11]
    }
    
    if stats:
        player_info['stats'] = {
            'season': stats[0],
            'games_played': stats[1],
            'ppg': float(stats[2]) if stats[2] else 0.0,
            'rpg': float(stats[3]) if stats[3] else 0.0,
            'apg': float(stats[4]) if stats[4] else 0.0,
            'fg_pct': float(stats[5]) if stats[5] else 0.0,
            'three_pt_pct': float(stats[6]) if stats[6] else 0.0
        }
    else:
        player_info['stats'] = None
        
    return jsonify(player_info)