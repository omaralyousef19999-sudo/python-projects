"""
واجهة ويب بسيطة باستخدام FastAPI لعرض بيانات أساسية ورفع CSV.
مناسبة لعرض الجداول والرسومات التي يولّدها reports.py
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from .database import init_db, get_conn
from . import reports, teams, matches, standings
import shutil
import os
import pandas as pd

app = FastAPI(title="UEFA CL Manager Dashboard")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/teams")
def api_list_teams():
    return teams.list_teams()

@app.get("/matches")
def api_list_matches():
    return matches.list_matches()

@app.get("/standings")
def api_standings():
    return standings.get_standings_by_group()

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    رفع CSV: متوقع صيغ: date,home_team,away_team,home_goals,away_goals,stage,stadium
    هذا endpoint يقوم بقراءة الصفوف وإدراجها كمباريات (سيبحث عن أسماء الفرق المدخلة).
    """
    tmp = f"/tmp/{file.filename}"
    with open(tmp, "wb") as f:
        shutil.copyfileobj(file.file, f)
    df = pd.read_csv(tmp)
    # توقع الأعمدة الأساسية
    for _, row in df.iterrows():
        # حاول إيجاد team ids بالاسم
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT team_id FROM teams WHERE name = ?", (row["home_team"],))
            ht = cur.fetchone()
            cur.execute("SELECT team_id FROM teams WHERE name = ?", (row["away_team"],))
            at = cur.fetchone()
            if ht and at:
                matches.add_match(home_team=int(ht[0]), away_team=int(at[0]), home_goals=int(row.get("home_goals",0) or 0), away_goals=int(row.get("away_goals",0) or 0), date=row.get("date"), stage=row.get("stage"), stadium=row.get("stadium"))
    os.remove(tmp)
    return {"status": "ok"}