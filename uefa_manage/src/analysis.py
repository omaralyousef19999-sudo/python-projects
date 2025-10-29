"""
وحدات تحليل إحصائي: مؤشرات الأداء لكل فريق وللاعبين.
يعتمد كثيراً على pandas لتسهيل التجميع والتحليل.
"""

from typing import Optional, Dict, Any
import pandas as pd
from .database import get_conn
import io


def teams_performance_summary(db: Optional[str] = None) -> Dict[str, Any]:
    """
    يرجع dict يحتوي summary لكل فريق: total goals for/against, points, played, winrate.
    """
    with get_conn(db) as conn:
        matches_df = pd.read_sql_query("SELECT m.*, th.name as home_name, ta.name as away_name FROM matches m JOIN teams th ON m.home_team = th.team_id JOIN teams ta ON m.away_team = ta.team_id", conn)
        standings_df = pd.read_sql_query("SELECT s.*, t.name FROM standings s JOIN teams t ON s.team_id = t.team_id", conn)
    # حساب مؤشرات مبسطة
    result = {}
    for _, row in standings_df.iterrows():
        name = row["name"]
        played = int(row["played"] or 0)
        points = int(row["points"] or 0)
        gf = int(row["goals_for"] or 0)
        ga = int(row["goals_against"] or 0)
        winrate = (int(row["wins"]) / played) if played > 0 else 0.0
        result[name] = {"played": played, "points": points, "goals_for": gf, "goals_against": ga, "winrate": round(winrate, 3)}
    # top scorers per team (total goals scored by team)
    team_goals = matches_df.groupby("home_name")["home_goals"].sum().add(matches_df.groupby("away_name")["away_goals"].sum(), fill_value=0)
    for t, goals in team_goals.items():
        if t in result:
            result[t]["goals_total"] = int(goals)
    return result


def timeseries_goals(db: Optional[str] = None):
    """
    يرسل DataFrame بالخانات date وgoals_total (مجمعة يومياً).
    """
    with get_conn(db) as conn:
        df = pd.read_sql_query("SELECT date, home_goals, away_goals FROM matches WHERE date IS NOT NULL", conn, parse_dates=["date"])
    if df.empty:
        return pd.DataFrame(columns=["date", "goals_total"])
    df["goals_total"] = df["home_goals"].fillna(0) + df["away_goals"].fillna(0)
    daily = df.groupby(df["date"].dt.date)["goals_total"].sum().reset_index().rename(columns={"date": "date"})
    return daily