-- Sample data for WNBA Draft Application
-- Run this after creating the schema to populate with sample records

-- Insert sample users
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@wnbadraft.com', 'hashed_password_here', 'admin'),
('scout_john', 'john.scout@wnbadraft.com', 'hashed_password_here', 'scout'),
('scout_jane', 'jane.scout@wnbadraft.com', 'hashed_password_here', 'scout'),
('user_mike', 'mike@wnbadraft.com', 'hashed_password_here', 'user'),
('user_sarah', 'sarah@wnbadraft.com', 'hashed_password_here', 'user');

-- Insert sample teams
INSERT INTO teams (team_name, city, conference) VALUES
('Aces', 'Las Vegas', 'Western'),
('Liberty', 'New York', 'Eastern'),
('Storm', 'Seattle', 'Western'),
('Sun', 'Connecticut', 'Eastern'),
('Lynx', 'Minnesota', 'Western'),
('Fever', 'Indiana', 'Eastern'),
('Wings', 'Dallas', 'Western'),
('Mercury', 'Phoenix', 'Western'),
('Sky', 'Chicago', 'Eastern'),
('Mystics', 'Washington', 'Eastern'),
('Sparks', 'Los Angeles', 'Western'),
('Dream', 'Atlanta', 'Eastern');

-- Insert sample players
INSERT INTO players (first_name, last_name, position, height, school, age, primary_team_id) VALUES
('Paige', 'Bueckers', 'PG', '6\'0\"', 'UConn', 22, NULL),
('Kiki', 'Iriafen', 'F', '6\'3\"', 'USC', 21, NULL),
('Madison', 'Booker', 'G', '5\'9\"', 'Texas', 22, NULL),
('Te-Hina', 'Paopao', 'G', '5\'9\"', 'South Carolina', 22, NULL),
('Dominique', 'Malonga', 'C', '6\'4\"', 'Syracuse', 23, NULL),
('Azzi', 'Fudd', 'G', '5\'11\"', 'UConn', 21, NULL),
('Aneesah', 'Morrow', 'F', '6\'1\"', 'LSU', 22, NULL),
('Olivia', 'Miles', 'PG', '5\'10\"', 'Notre Dame', 21, NULL),
('Lauren', 'Betts', 'C', '6\'7\"', 'UCLA', 20, NULL),
('Georgia', 'Amoore', 'PG', '5\'6\"', 'Kentucky', 22, NULL);

-- Insert sample player stats
INSERT INTO player_stats (player_id, season, games_played, ppg, rpg, apg, fg_pct, three_pt_pct) VALUES
(1, '2023-24', 31, 21.9, 5.2, 3.8, 0.527, 0.414),
(2, '2024-25', 28, 18.7, 11.1, 2.4, 0.544, 0.367),
(3, '2024-25', 30, 15.8, 3.9, 4.2, 0.478, 0.392),
(4, '2024-25', 32, 12.4, 2.8, 5.1, 0.491, 0.378),
(5, '2024-25', 29, 14.2, 8.6, 1.8, 0.523, 0.298),
(6, '2024-25', 27, 16.7, 4.1, 2.9, 0.465, 0.402),
(7, '2024-25', 33, 19.3, 9.8, 2.2, 0.556, 0.267),
(8, '2024-25', 31, 13.8, 3.7, 6.4, 0.489, 0.341),
(9, '2024-25', 30, 12.1, 11.4, 1.9, 0.578, 0.000),
(10, '2024-25', 32, 14.6, 2.1, 7.2, 0.445, 0.389);

-- Insert sample scouting reports
INSERT INTO scouting_reports (player_id, user_id, strengths, weaknesses, projection) VALUES
(1, 2, 'Elite playmaker with excellent court vision. Clutch performer and leader.', 'Injury history concerns. Needs to improve defensive consistency.', 'Franchise cornerstone - #1 overall pick'),
(2, 2, 'Versatile forward with excellent rebounding instincts. Strong post presence.', 'Limited perimeter shooting. Needs to improve ball handling.', 'Top 5 pick with immediate impact potential'),
(3, 3, 'Explosive scorer with deep range. Great in transition.', 'Defensive lapses. Shot selection can be questionable at times.', 'Lottery pick with high scoring upside'),
(4, 3, 'Outstanding floor general with high basketball IQ. Excellent passer.', 'Lacks ideal size for position. Turnover prone under pressure.', 'Mid-first round - solid starter potential'),
(5, 2, 'Dominant paint presence with excellent shot-blocking ability.', 'Limited offensive range. Needs to improve free throw shooting.', 'First round - defensive anchor potential'),
(6, 3, 'Pure shooter with excellent range. High basketball IQ.', 'Injury concerns limit availability. Needs to improve athleticism.', 'High risk, high reward pick'),
(7, 2, 'Elite rebounder with improving offensive skills. Great motor.', 'Limited shooting range. Needs to develop perimeter game.', 'Solid first round pick - double-double potential'),
(8, 3, 'Quick point guard with excellent leadership qualities.', 'Small stature limits defensive impact. Needs to improve outside shot.', 'Late first round - backup PG potential'),
(9, 2, 'Exceptional size for the position with good touch around rim.', 'Needs significant development time. Limited mobility.', 'Project pick with upside'),
(10, 3, 'Dynamic point guard with excellent speed and court vision.', 'Size concerns at next level. Needs to add strength.', 'Second round potential starter');

-- Insert sample mock drafts
INSERT INTO mock_drafts (user_id, mock_name) VALUES
(2, 'John\'s 2025 WNBA Mock Draft v1'),
(3, 'Jane\'s Top 10 Prospects'),
(4, 'Mike\'s Dream Draft'),
(5, 'Sarah\'s Realistic Mock'),
(2, 'John\'s Updated Mock v2');

-- Insert sample mock draft picks
INSERT INTO mock_draft_picks (mock_id, player_id, round, pick_number, target_team_id) VALUES
(1, 2, 1, 1, 1),
(1, 3, 1, 2, 2),
(1, 4, 1, 3, 3),
(1, 5, 1, 4, 4),
(1, 6, 1, 5, 5),
(2, 1, 1, 1, 6),
(2, 2, 1, 2, 7),
(2, 3, 1, 3, 8),
(2, 4, 1, 4, 9),
(2, 5, 1, 5, 10),
(3, 2, 1, 1, 2),
(3, 1, 1, 2, 4),
(3, 3, 1, 3, 6),
(3, 5, 1, 4, 8),
(3, 4, 1, 5, 10),
(4, 4, 1, 1, 1),
(4, 2, 1, 2, 3),
(4, 3, 1, 3, 5),
(4, 6, 1, 4, 7),
(4, 7, 1, 5, 9),
(5, 2, 1, 1, 1),
(5, 1, 1, 2, 2),
(5, 3, 1, 3, 3),
(5, 4, 1, 4, 4),
(5, 5, 1, 5, 5);