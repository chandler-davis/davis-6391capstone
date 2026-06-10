from flask import Blueprint, render_template, request, jsonify
from app.db_connect import get_db
from app.blueprints.auth import login_required

stats = Blueprint('stats', __name__)

@stats.route('/')
@login_required
def show_stats():
    """Display comprehensive stats dashboard with charts and analytics"""
    db = get_db()
    cursor = db.cursor()
    
    # Get all player stats for current season
    cursor.execute('''
        SELECT p.player_id, p.first_name, p.last_name, p.position, p.school, p.age,
               ps.games_played, ps.ppg, ps.rpg, ps.apg, ps.fg_pct, ps.three_pt_pct
        FROM players p
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id AND ps.season = '2024-25'
        ORDER BY ps.ppg DESC
    ''')
    
    all_player_stats = cursor.fetchall()
    
    # Get summary statistics
    cursor.execute('''
        SELECT
            COUNT(*) as total_players,
            AVG(ps.ppg) as avg_ppg,
            AVG(ps.rpg) as avg_rpg,
            AVG(ps.apg) as avg_apg,
            AVG(ps.fg_pct) as avg_fg_pct,
            AVG(ps.three_pt_pct) as avg_three_pt_pct
        FROM player_stats ps
        WHERE ps.season = '2024-25' AND ps.games_played > 0
    ''')
    
    summary_stats = cursor.fetchone()
    
    return render_template('stats/stats.html', 
                         all_player_stats=all_player_stats,
                         summary_stats=summary_stats)

@stats.route('/api/chart-data')
@login_required
def get_chart_data():
    """API endpoint for chart data"""
    chart_type = request.args.get('type', 'ppg')
    
    db = get_db()
    cursor = db.cursor()
    
    if chart_type == 'ppg':
        cursor.execute('''
            SELECT p.first_name, p.last_name, ps.ppg, p.position
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            WHERE ps.season = '2024-25' AND ps.games_played > 0
            ORDER BY ps.ppg DESC
            LIMIT 10
        ''')
    elif chart_type == 'fg_pct':
        cursor.execute('''
            SELECT p.first_name, p.last_name, ps.fg_pct, p.position
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            WHERE ps.season = '2024-25' AND ps.games_played > 5
            ORDER BY ps.fg_pct DESC
            LIMIT 10
        ''')
    elif chart_type == 'three_pt_pct':
        cursor.execute('''
            SELECT p.first_name, p.last_name, ps.three_pt_pct, p.position
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            WHERE ps.season = '2024-25' AND ps.games_played > 5
            ORDER BY ps.three_pt_pct DESC
            LIMIT 10
        ''')
    elif chart_type == 'position':
        cursor.execute('''
            SELECT p.position,
                   COUNT(*) as player_count,
                   AVG(ps.ppg) as avg_ppg,
                   AVG(ps.rpg) as avg_rpg,
                   AVG(ps.apg) as avg_apg
            FROM players p
            LEFT JOIN player_stats ps ON p.player_id = ps.player_id AND ps.season = '2024-25'
            GROUP BY p.position
            ORDER BY p.position
        ''')
    else:
        return jsonify({'error': 'Invalid chart type'}), 400
    
    data = cursor.fetchall()
    
    # Format data for charts
    if chart_type == 'position':
        formatted_data = [{
            'position': row[0],
            'player_count': row[1],
            'avg_ppg': float(row[2]) if row[2] else 0,
            'avg_rpg': float(row[3]) if row[3] else 0,
            'avg_apg': float(row[4]) if row[4] else 0
        } for row in data]
    else:
        formatted_data = [{
            'name': f"{row[0]} {row[1]}",
            'value': float(row[2]) if row[2] else 0,
            'position': row[3]
        } for row in data]
    
    return jsonify(formatted_data)

@stats.route('/api/top-performers')
@login_required
def get_top_performers():
    """Get top performers in various categories"""
    db = get_db()
    cursor = db.cursor()
    
    # Top scorers
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.position, p.school, ps.ppg
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.season = '2024-25' AND ps.games_played > 0
        ORDER BY ps.ppg DESC
        LIMIT 5
    ''')
    top_scorers = cursor.fetchall()

    # Most efficient shooters (FG%)
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.position, p.school, ps.fg_pct
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.season = '2024-25' AND ps.games_played > 5
        ORDER BY ps.fg_pct DESC
        LIMIT 5
    ''')
    efficient_shooters = cursor.fetchall()

    # Best 3-point shooters
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.position, p.school, ps.three_pt_pct
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.season = '2024-25' AND ps.games_played > 5
        ORDER BY ps.three_pt_pct DESC
        LIMIT 5
    ''')
    three_point_leaders = cursor.fetchall()

    # Top rebounders
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.position, p.school, ps.rpg
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.season = '2024-25' AND ps.games_played > 0
        ORDER BY ps.rpg DESC
        LIMIT 5
    ''')
    top_rebounders = cursor.fetchall()

    # Top assists
    cursor.execute('''
        SELECT p.first_name, p.last_name, p.position, p.school, ps.apg
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.season = '2024-25' AND ps.games_played > 0
        ORDER BY ps.apg DESC
        LIMIT 5
    ''')
    top_assists = cursor.fetchall()
    
    return jsonify({
        'top_scorers': [{'name': f"{row[0]} {row[1]}", 'position': row[2], 'school': row[3], 'value': float(row[4])} for row in top_scorers],
        'efficient_shooters': [{'name': f"{row[0]} {row[1]}", 'position': row[2], 'school': row[3], 'value': float(row[4])*100} for row in efficient_shooters],
        'three_point_leaders': [{'name': f"{row[0]} {row[1]}", 'position': row[2], 'school': row[3], 'value': float(row[4])*100} for row in three_point_leaders],
        'top_rebounders': [{'name': f"{row[0]} {row[1]}", 'position': row[2], 'school': row[3], 'value': float(row[4])} for row in top_rebounders],
        'top_assists': [{'name': f"{row[0]} {row[1]}", 'position': row[2], 'school': row[3], 'value': float(row[4])} for row in top_assists]
    })