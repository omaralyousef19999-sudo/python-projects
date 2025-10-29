"""
إدارة اللاعبين: إضافة واسترجاع
"""

from typing import Optional, List, Dict
from .database import get_conn


def add_player(name: str, position: Optional[str], age: Optional[int], team_id: Optional[int], db: Optional[str] = None) -> int:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO players(name, position, age, team_id) VALUES (?, ?, ?, ?)",
            (name, position, age, team_id),
        )
        return cur.lastrowid


def list_players(team_id: Optional[int] = None, db: Optional[str] = None) -> List[Dict]:
    with get_conn(db) as conn:
        cur = conn.cursor()
        if team_id:
            cur.execute("SELECT player_id, name, position, age, team_id FROM players WHERE team_id = ?", (team_id,))
        else:
            cur.execute("SELECT player_id, name, position, age, team_id FROM players")
        keys = ["player_id", "name", "position", "age", "team_id"]
        return [dict(zip(keys, r)) for r in cur.fetchall()]