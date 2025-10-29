"""
تسجيل المباريات واستعلام عنها. تحديثات مبسطة للـstandings تتم في module standings.py.
"""

from typing import Optional, List, Dict
from .database import get_conn
from .models import Match
from .standings import recalc_standings_for_match

def add_match(home_team: int, away_team: int, home_goals: int = 0, away_goals: int = 0, date: Optional[str] = None, stage: Optional[str] = None, stadium: Optional[str] = None, db: Optional[str] = None) -> int:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO matches(home_team, away_team, home_goals, away_goals, date, stage, stadium) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (home_team, away_team, home_goals, away_goals, date, stage, stadium),
        )
        match_id = cur.lastrowid
    # بعد الإضافة نعيد حساب ترتيب الفرق المتأثرة
    recalc_standings_for_match(match_id, db=db)
    return match_id


def update_match_result(match_id: int, home_goals: int, away_goals: int, db: Optional[str] = None) -> None:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE matches SET home_goals = ?, away_goals = ? WHERE match_id = ?", (home_goals, away_goals, match_id))
    recalc_standings_for_match(match_id, db=db)


def list_matches(db: Optional[str] = None) -> List[Dict]:
    with get_conn(db) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT match_id, home_team, away_team, home_goals, away_goals, date, stage, stadium FROM matches ORDER BY date IS NULL, date""")
        keys = ["match_id", "home_team", "away_team", "home_goals", "away_goals", "date", "stage", "stadium"]
        return [dict(zip(keys, r)) for r in cur.fetchall()]