"""
Typer-based CLI: import CSV, list entities, show standings, generate reports.
"""

from typing import Optional
import typer
from .database import init_db
from . import teams, players, matches, standings, reports
import csv
import os

app = typer.Typer(help="UEFA Champions League Manager CLI")


@app.command()
def init(db: Optional[str] = typer.Option(None, help="path to sqlite db")):
    """
    انشئ قاعدة البيانات (إن لم توجد).
    """
    path = init_db(db)
    typer.echo(f"Database initialized at {path}")


@app.command("add-team")
def cli_add_team(name: str, country: Optional[str] = None, ranking: Optional[int] = None, group: Optional[str] = None, db: Optional[str] = None):
    tid = teams.add_team(name=name, country=country, ranking=ranking, group_name=group, db=db)
    typer.echo(f"Team added/exists with id {tid}")


@app.command("list-teams")
def cli_list_teams(db: Optional[str] = None):
    t = teams.list_teams(db=db)
    for row in t:
        typer.echo(f"{row['team_id']}: {row['name']} ({row.get('country')}) group={row.get('group_name')}")


@app.command("import-csv")
def import_csv(path: str, db: Optional[str] = None):
    """
    استيراد بيانات من CSV بصيغة مريحة:
    توقع الأعمدة: stage,date,stadium,home_team,away_team,home_goals,away_goals
    سيبحث عن أسماء الفرق الموجودة ويضيف مباريات.
    """
    if not os.path.exists(path):
        typer.echo("CSV not found")
        raise typer.Exit(code=1)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # تأكد من وجود الفرق في جدول teams
            from .database import get_conn
            with get_conn(db) as conn:
                cur = conn.cursor()
                cur.execute("SELECT team_id FROM teams WHERE name = ?", (r["home_team"],))
                ht = cur.fetchone()
                cur.execute("SELECT team_id FROM teams WHERE name = ?", (r["away_team"],))
                at = cur.fetchone()
                if not ht or not at:
                    typer.echo(f"Skipping match (team not found): {r.get('home_team')} vs {r.get('away_team')}")
                    continue
                from .matches import add_match
                add_match(home_team=int(ht[0]), away_team=int(at[0]), home_goals=int(r.get("home_goals") or 0), away_goals=int(r.get("away_goals") or 0), date=r.get("date"), stage=r.get("stage"), stadium=r.get("stadium"), db=db)
    typer.echo("CSV import completed.")


@app.command("standings")
def cli_standings(group: Optional[str] = None, db: Optional[str] = None, out: Optional[str] = None):
    """
    عرض الترتيب (يمكن حفظه إلى out folder تلقائياً عبر reports).
    """
    st = standings.get_standings_by_group(group_name=group, db=db)
    for row in st:
        if group:
            typer.echo(f"{row['name']}: {row['points']} pts, GF:{row['goals_for']} GA:{row['goals_against']}")
        else:
            typer.echo(f"{row['group_name']} | {row['name']}: {row['points']} pts, GF:{row['goals_for']} GA:{row['goals_against']}")
    if out:
        # توليد تقارير سريعة
        reports.export_summary_json(db=db, out=out)
        reports.export_summary_csv(db=db, out=out)
        reports.plot_top_teams(db=db, out=out)
        typer.echo(f"Saved reports to {out}")


@app.command("generate-reports")
def cli_generate_reports(db: Optional[str] = None, out: Optional[str] = "out"):
    p1 = reports.export_summary_json(db=db, out=out)
    p2 = reports.export_summary_csv(db=db, out=out)
    p3 = reports.plot_top_teams(db=db, out=out)
    p4 = reports.plot_goals_timeseries(db=db, out=out)
    try:
        p5 = reports.export_pdf_report(db=db, out=out)
    except Exception as e:
        p5 = None
    typer.echo("Reports generated:")
    for p in (p1, p2, p3, p4, p5):
        if p:
            typer.echo(f" - {p}")


def run():
    app()