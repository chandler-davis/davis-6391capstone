# WNBA Draft Management System

A comprehensive web application for managing WNBA draft prospects, tracking player statistics, creating mock drafts, and generating scouting reports.

## Features

### Player Management
- View and manage draft prospect profiles
- Track player information (position, height, school, age)
- Associate players with WNBA teams
- Real-time player data updates

### Statistics Dashboard
- Comprehensive 2024-25 season statistics
- Interactive charts and visualizations
- Top performers leaderboards (scoring, shooting, rebounding, assists)
- Position-based analytics
- League-wide summary statistics

### Mock Drafts
- Create and manage multiple mock draft scenarios
- Drag-and-drop draft board interface
- Assign prospects to teams with round/pick numbers
- Save and compare different draft scenarios

### Scouting Reports
- Create detailed player evaluations
- Document strengths and weaknesses
- Project draft positions
- Track scout contributions

### Teams Management
- View all 12 WNBA teams
- Conference organization (Eastern/Western)
- Team roster tracking

## Tech Stack

- **Backend**: Flask (Python 3.12)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Authentication**: Flask sessions with Werkzeug password hashing

## Installation

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone git@github.com:chandler-davis/davis-6391capstone.git
cd davis-6391capstone
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database:
- Update `.env` file with your MySQL credentials:
```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wnba_draft
DB_PORT=3306
```

5. Set up the database:
```bash
python setup_database.py
```

6. Update demo credentials (optional):
```bash
python update_demo_credentials.py
```

## Usage

### Running the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

### Demo Credentials

**Username:** admin123
**Password:** scout123

### User Roles
- **Admin**: Full access to all features
- **Scout**: Can create/edit scouting reports and mock drafts
- **User**: Read-only access to player data and statistics

## Project Structure

```
davis-6391capstone/
├── app/
│   ├── blueprints/          # Route handlers
│   │   ├── auth.py          # Authentication
│   │   ├── players.py       # Player management
│   │   ├── stats.py         # Statistics & analytics
│   │   ├── teams.py         # Team management
│   │   └── mock_drafts.py   # Mock draft creation
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── db_connect.py        # Database connection
│   └── app_factory.py       # Flask app factory
├── database/
│   ├── schema.sql           # Database schema
│   └── seed_data.sql        # Sample data
├── app.py                   # Application entry point
├── setup_database.py        # Database setup script
├── requirements.txt         # Python dependencies
└── .env                     # Environment configuration
```

## Database Schema

### Core Tables
- **users**: User accounts and authentication
- **players**: Draft prospect information
- **player_stats**: Season statistics
- **teams**: WNBA team information
- **scouting_reports**: Scout evaluations
- **mock_drafts**: Draft scenarios
- **mock_draft_picks**: Individual draft selections

## API Endpoints

### Statistics
- `GET /stats/` - Statistics dashboard
- `GET /stats/api/chart-data?type={ppg|fg_pct|three_pt_pct|position}` - Chart data
- `GET /stats/api/top-performers` - Leaderboards

### Players
- `GET /players/` - Player listing
- `POST /players/` - Add new player
- `POST /players/update_player/<id>` - Update player
- `DELETE /players/delete_player/<id>` - Delete player
- `GET /players/api/player/<id>` - Player details

### Mock Drafts
- `GET /mock-drafts/` - List all mock drafts
- `POST /mock-drafts/create` - Create new mock draft
- `GET /mock-drafts/view/<id>` - View mock draft
- `POST /mock-drafts/save-picks` - Save draft selections

## Development

### Adding New Features
See `CLAUDE_RULES.md` for development guidelines and best practices.

### Database Migrations
After modifying `schema.sql`, run:
```bash
python setup_database.py
```

## License

This project is part of a capstone project for educational purposes.