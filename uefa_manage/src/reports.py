"""
توليد تقارير: JSON, CSV, PNG, PDF.
"""


from typing import Optional
import json
import os
import csv
from .analysis import teams_performance_summary, timeseries_goals
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

def ensure_outdir(out: str):
    if not os.path.exists(out):
        os.makedirs(out, exist_ok=True)

def export_summary_json(db: Optional[str], out: str = "out"):
    ensure_outdir(out)
    summary = teams_performance_summary(db=db)
    path = os.path.join(out, "summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": pd.Timestamp.now().isoformat(), "teams": summary}, f, ensure_ascii=False, indent=2)
    return path

def export_summary_csv(db: Optional[str], out: str = "out"):
    ensure_outdir(out)
    summary = teams_performance_summary(db=db)
    path = os.path.join(out, "summary.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["team", "played", "points", "goals_for", "goals_against", "winrate", "goals_total"]
        writer.writerow(header)
        for team, vals in summary.items():
            row = [team, vals.get("played", 0), vals.get("points", 0), vals.get("goals_for", 0), vals.get("goals_against", 0), vals.get("winrate", 0), vals.get("goals_total", 0)]
            writer.writerow(row)
    return path

def plot_top_teams(db: Optional[str], out: str = "out", top_n: int = 10):
    ensure_outdir(out)
    summary = teams_performance_summary(db=db)
    df = pd.DataFrame.from_dict(summary, orient="index").fillna(0)
    if df.empty:
        return None
    df_sorted = df.sort_values("goals_total", ascending=False).head(top_n)
    plt.figure(figsize=(10,6))
    df_sorted["goals_total"].plot(kind="bar")
    plt.title("Top Teams by Goals")
    plt.tight_layout()
    path = os.path.join(out, "top_teams_goals.png")
    plt.savefig(path)
    plt.close()
    return path

def plot_goals_timeseries(db: Optional[str], out: str = "out"):
    ensure_outdir(out)
    df = timeseries_goals(db=db)
    if df.empty:
        return None
    plt.figure(figsize=(10,5))
    plt.plot(df["date"], df["goals_total"], marker="o")
    plt.title("Goals Time Series")
    plt.tight_layout()
    path = os.path.join(out, "goals_timeseries.png")
    plt.savefig(path)
    plt.close()
    return path

def export_pdf_report(db: Optional[str], out: str = "out"):
    """
    يولّد تقرير PDF بسيط يجمع الـsummary وبعض الصور إذا وُجدت.
    """
    ensure_outdir(out)
    summary_path = export_summary_json(db=db, out=out)
    top_png = plot_top_teams(db=db, out=out)
    ts_png = plot_goals_timeseries(db=db, out=out)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "UEFA Champions League - Report", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Generated: {pd.Timestamp.now().isoformat()}", ln=True)
    pdf.ln(4)
    # include summary snippet
    with open(summary_path, "r", encoding="utf-8") as f:
        js = json.load(f)
    pdf.multi_cell(0, 6, f"Teams count: {len(js.get('teams',{}))}")
    pdf.ln(4)
    # images
    if top_png and os.path.exists(top_png):
        pdf.image(top_png, w=170)
        pdf.ln(4)
    if ts_png and os.path.exists(ts_png):
        pdf.add_page()
        pdf.image(ts_png, w=170)
    out_pdf = os.path.join(out, "report.pdf")
    pdf.output(out_pdf)
    return out_pdf