"""
إدارة الفرق: إضافة، تعديل، حذف، واستعلام.
"""

from typing import Optional, List, Dict
from .database import get_conn
from .models import Team


def add_team(name: str, country: Optional[str] = None, ranking: Optional[int] = None, group_name: Optional[str] = None, db: Optional[str] = None) -> int:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO teams(name, country, ranking, group_name) VALUES (?, ?, ?, ?)",
            (name, country, ranking, group_name),
        )
        conn.commit()
        cur.execute("SELECT team_id FROM teams WHERE name = ?", (name,))
        row = cur.fetchone()
        return row[0]


def get_team_by_name(name: str, db: Optional[str] = None) -> Optional[Dict]:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT team_id, name, country, ranking, group_name FROM teams WHERE name = ?", (name,))
        r = cur.fetchone()
        if not r:
            return None
        keys = ["team_id", "name", "country", "ranking", "group_name"]
        return dict(zip(keys, r))


def list_teams(db: Optional[str] = None) -> List[Dict]:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT team_id, name, country, ranking, group_name FROM teams ORDER BY name")
        rows = cur.fetchall()
        keys = ["team_id", "name", "country", "ranking", "group_name"]
        return [dict(zip(keys, r)) for r in rows]