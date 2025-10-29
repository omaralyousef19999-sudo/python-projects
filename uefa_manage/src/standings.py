"""
حساب الترتيب داخل المجموعات. هذه نسخة معيارية: نعيد ضبط standings ونحسب من جدول matches.
يُراعى معيار النقاط ثم فارق الأهداف ثم الأهداف المسجلة. للمطابقة التامة مع قواعد UEFA
قد نحتاج إضافة معيار المواجهات المباشرة (head-to-head) لاحقاً.
"""

from typing import Optional
from .database import get_conn
import collections


def recalc_all_standings(db: Optional[str] = None) -> None:
    """
    إعادة حساب كامل للـstandings من الصفر استناداً إلى جدول matches.
    """
    with get_conn(db) as conn:
        cur = conn.cursor()
        # امسح standings
        cur.execute("DELETE FROM standings")
        # احصل كل الفرق
        cur.execute("SELECT team_id, group_name FROM teams")
        teams = cur.fetchall()
        for team_id, group_name in teams:
            cur.execute(
                "INSERT OR REPLACE INTO standings(team_id, played, wins, draws, losses, goals_for, goals_against, points, group_name) VALUES (?,0,0,0,0,0,0,0,?)",
                (team_id, group_name),
            )
        # process each match
        cur.execute("SELECT home_team, away_team, home_goals, away_goals FROM matches WHERE home_goals IS NOT NULL AND away_goals IS NOT NULL")
        for home_team, away_team, hg, ag in cur.fetchall():
            _apply_result(cur, home_team, away_team, hg, ag)
        conn.commit()


def recalc_standings_for_match(match_id: int, db: Optional[str] = None) -> None:
    """
    إعادة حساب شامل: أبسط طريقة مضمونة للاتساق: إعادة حساب كل شيء.
    """
    recalc_all_standings(db=db)


def _apply_result(cur, home_team: int, away_team: int, hg: int, ag: int):
    # تحديث مبادئ اللعب
    # played
    cur.execute("UPDATE standings SET played = played + 1 WHERE team_id IN (?, ?)", (home_team, away_team))
    # goals
    cur.execute("UPDATE standings SET goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?", (hg, ag, home_team))
    cur.execute("UPDATE standings SET goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?", (ag, hg, away_team))
    # نتائج
    if hg > ag:
        # home win
        cur.execute("UPDATE standings SET wins = wins + 1, points = points + 3 WHERE team_id = ?", (home_team,))
        cur.execute("UPDATE standings SET losses = losses + 1 WHERE team_id = ?", (away_team,))
    elif hg < ag:
        cur.execute("UPDATE standings SET wins = wins + 1, points = points + 3 WHERE team_id = ?", (away_team,))
        cur.execute("UPDATE standings SET losses = losses + 1 WHERE team_id = ?", (home_team,))
    else:
        # draw
        cur.execute("UPDATE standings SET draws = draws + 1, points = points + 1 WHERE team_id IN (?, ?)", (home_team, away_team))


def get_standings_by_group(group_name: Optional[str] = None, db: Optional[str] = None):
    with get_conn(db) as conn:
        cur = conn.cursor()
        if group_name:
            cur.execute(
                "SELECT s.team_id, t.name, s.played, s.wins, s.draws, s.losses, s.goals_for, s.goals_against, s.points FROM standings s JOIN teams t ON s.team_id = t.team_id WHERE s.group_name = ? ORDER BY s.points DESC, (s.goals_for - s.goals_against) DESC, s.goals_for DESC",
                (group_name,),
            )
        else:
            cur.execute(
                "SELECT s.team_id, t.name, s.played, s.wins, s.draws, s.losses, s.goals_for, s.goals_against, s.points, s.group_name FROM standings s JOIN teams t ON s.team_id = t.team_id ORDER BY s.group_name, s.points DESC, (s.goals_for - s.goals_against) DESC, s.goals_for DESC"
            )
        keys = ["team_id", "name", "played", "wins", "draws", "losses", "goals_for", "goals_against", "points"]
        rows = cur.fetchall()
        # if group_name supplied no group col; otherwise include group
        if group_name:
            return [dict(zip(keys, r)) for r in rows]
        else:
            keys = ["team_id", "name", "played", "wins", "draws", "losses", "goals_for", "goals_against", "points", "group_name"]
            return [dict(zip(keys, r)) for r in rows]