DROP TABLE IF EXISTS teams;

CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  abbreviation TEXT,
  location TEXT
);

DROP TABLE IF EXISTS players;

CREATE TABLE IF NOT EXISTS players (
  player_id INTEGER PRIMARY KEY,
  team_id INTEGER,
  firstName TEXT,
  lastName TEXT,
  unit TEXT,
  position TEXT,
  weight INTEGER,
  height TEXT,
  age INTEGER,
  dob TEXT,
  college TEXT,
  FOREIGN KEY (team_id) REFERENCES teams(team_id)
);