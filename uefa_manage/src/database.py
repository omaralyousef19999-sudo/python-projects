"""
database.py
مسؤول عن إنشاء اتصال SQLite وإعداد الجداول الأساسية.
يستخدم sqlite3 من مكتبة بايثون القياسية لتجنّب تبعيات ORM إضافية.
"""

from typing import Optional
import sqlite3
import os
from contextlib import contextmanager

DEFAULT_DB = "db.sqlite"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT,
    ranking INTEGER,
    group_name TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT,
    age INTEGER,
    team_id INTEGER,
    FOREIGN KEY(team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_team INTEGER NOT NULL,
    away_team INTEGER NOT NULL,
    home_goals INTEGER DEFAULT 0,
    away_goals INTEGER DEFAULT 0,
    date TEXT,
    stage TEXT,
    stadium TEXT,
    FOREIGN KEY(home_team) REFERENCES teams(team_id),
    FOREIGN KEY(away_team) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS standings (
    team_id INTEGER PRIMARY KEY,
    played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    group_name TEXT,
    FOREIGN KEY(team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS statistics (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    FOREIGN KEY(player_id) REFERENCES players(player_id) ON DELETE CASCADE
);
"""


def init_db(db_path: Optional[str] = None) -> str:
    """
    Ensure database file and schema exist. Returns db_path used.
    """
    if db_path is None:
        db_path = DEFAULT_DB
    created = False
    if not os.path.exists(db_path):
        created = True
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    return db_path


@contextmanager
def get_conn(db_path: Optional[str] = None):
    if db_path is None:
        db_path = DEFAULT_DB
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()