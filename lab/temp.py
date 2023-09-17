from pathlib import Path
DIR = Path(__file__).resolve().parent.parent
print(DIR / "db.sqlite3")
