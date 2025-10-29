# src/__init__.py
"""
UEFA CL Manager - src package
يجمع كل الوحدات معًا لتسهيل الاستيراد
"""

# استيراد الدوال الرئيسية من كل ملف
from .database import init_db, get_conn
from .teams import add_team, list_teams
from .matches import add_match, list_matches
from .standings import (
    recalc_all_standings,
    get_standings_by_group,
    get_standings_all
)
from .reports import (
    export_summary_json,
    export_summary_csv,
    export_summary_pdf,
    export_summary_png
)
from .analysis import (
    teams_performance_summary,
    timeseries_goals,
    player_stats
)

# اختياري: جعل الكل متاح عند استيراد src.*
all = [
    "init_db", "get_conn",
    "add_team", "list_teams",
    "add_match", "list_matches",
    "recalc_all_standings", "get_standings_by_group", "get_standings_all",
    "export_summary_json", "export_summary_csv", "export_summary_pdf", "export_summary_png",
    "teams_performance_summary", "timeseries_goals", "player_stats"
]