# UEFA Champions League Management & Analysis System (Minimal)

## متطلبات
Python 3.11+

تثبيت الحزم:
```bash
pip install -r requirements.txt
python -m src.main --help
python -m src.main import-csv examples/sample_data.csv --db db.sqlite
python -m src.main standings --db db.sqlite --out out/
python -m src.main generate-reports --db db.sqlite --out out/
uvicorn src.dashboard:app --reload --port 8000
pytest -q
---

الآن الملفات البرمجية — الصق كل قطعة في ملف مستقل حسب المسار.

---

## src/__init__.py
```python
# package marker