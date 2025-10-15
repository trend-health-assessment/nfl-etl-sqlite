PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
  team_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  abbreviation TEXT,
  conference TEXT,
  division TEXT
);

CREATE TABLE IF NOT EXISTS players (
  player_id TEXT PRIMARY KEY,
  full_name TEXT NOT NULL,
  position TEXT,
  team_id TEXT,
  height TEXT,
  weight TEXT,
  college TEXT,
  FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  week INTEGER,
  season INTEGER,
  home_team TEXT,
  away_team TEXT,
  game_date TEXT
);

CREATE TABLE IF NOT EXISTS player_stats (
  game_id TEXT,
  player_id TEXT,
  passing_yards REAL,
  rushing_yards REAL,
  receiving_yards REAL,
  touchdowns INTEGER,
  interceptions INTEGER,
  fantasy_points REAL,
  PRIMARY KEY (game_id, player_id),
  FOREIGN KEY (game_id) REFERENCES games(game_id),
  FOREIGN KEY (player_id) REFERENCES players(player_id)
);
