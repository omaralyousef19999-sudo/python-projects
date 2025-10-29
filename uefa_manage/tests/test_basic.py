"""
اختبار بسيط: init db, add teams, add matches, recalc standings runs without exception.
"""

import os
from src.database import init_db, get_conn
from src.teams import add_team, list_teams
from src.matches import add_match
from src.standings import recalc_all_standings, get_standings_by_group

DB_TEST = "test_db.sqlite"

def test_basic_flow(tmp_path):
    db = tmp_path / DB_TEST
    db_path = str(db)
    init_db(db_path)
    t1 = add_team("Team A", country="Country A", group_name="Group 1", db=db_path)
    t2 = add_team("Team B", country="Country B", group_name="Group 1", db=db_path)
    assert t1 and t2
    m = add_match(home_team=t1, away_team=t2, home_goals=2, away_goals=1, date="2025-09-01", stage="Group", db=db_path)
    # recalc and fetch standings
    recalc_all_standings(db=db_path)
    st = get_standings_by_group(group_name="Group 1", db=db_path)
    assert len(st) == 2
    # cleanup
    os.remove(db_path)