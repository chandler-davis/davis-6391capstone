-- Database Schema for WNBA Draft Application
-- Run this file to create the required database structure

-- Drop existing tables if they exist (in reverse order due to foreign key constraints)
DROP TABLE IF EXISTS mock_draft_picks;
DROP TABLE IF EXISTS mock_drafts;
DROP TABLE IF EXISTS scouting_reports;
DROP TABLE IF EXISTS player_stats;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'scout', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create teams table
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    conference ENUM('Eastern', 'Western') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create players table
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position ENUM('PG', 'SG', 'SF', 'PF', 'C') NOT NULL,
    height VARCHAR(10),
    school VARCHAR(100),
    age INT,
    primary_team_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (primary_team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- Create player_stats table
CREATE TABLE player_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    season VARCHAR(10) NOT NULL,
    games_played INT DEFAULT 0,
    ppg DECIMAL(5,2) DEFAULT 0.00,
    rpg DECIMAL(5,2) DEFAULT 0.00,
    apg DECIMAL(5,2) DEFAULT 0.00,
    fg_pct DECIMAL(5,3) DEFAULT 0.000,
    three_pt_pct DECIMAL(5,3) DEFAULT 0.000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    UNIQUE KEY unique_player_season (player_id, season)
);

-- Create scouting_reports table
CREATE TABLE scouting_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    user_id INT NOT NULL,
    strengths TEXT,
    weaknesses TEXT,
    projection TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create mock_drafts table
CREATE TABLE mock_drafts (
    mock_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    mock_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create mock_draft_picks table (join table for many-to-many relationship)
CREATE TABLE mock_draft_picks (
    pick_id INT AUTO_INCREMENT PRIMARY KEY,
    mock_id INT NOT NULL,
    player_id INT NOT NULL,
    round INT NOT NULL,
    pick_number INT NOT NULL,
    target_team_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mock_id) REFERENCES mock_drafts(mock_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (target_team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    UNIQUE KEY unique_mock_pick (mock_id, round, pick_number)
);

-- Create indexes for improved query performance
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_teams_name ON teams (team_name);
CREATE INDEX idx_players_name ON players (last_name, first_name);
CREATE INDEX idx_players_position ON players (position);
CREATE INDEX idx_players_team ON players (primary_team_id);
CREATE INDEX idx_player_stats_player ON player_stats (player_id);
CREATE INDEX idx_player_stats_season ON player_stats (season);
CREATE INDEX idx_scouting_reports_player ON scouting_reports (player_id);
CREATE INDEX idx_scouting_reports_user ON scouting_reports (user_id);
CREATE INDEX idx_mock_drafts_user ON mock_drafts (user_id);
CREATE INDEX idx_mock_draft_picks_mock ON mock_draft_picks (mock_id);
CREATE INDEX idx_mock_draft_picks_player ON mock_draft_picks (player_id);