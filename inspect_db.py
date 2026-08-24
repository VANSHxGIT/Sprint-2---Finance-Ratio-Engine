import sqlite3
from pathlib import Path

DB_PATH = Path("database/nifty100.db")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)

tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""").fetchall()

print("\nDATABASE TABLES")
print("=" * 50)

for (table,) in tables:
    count = conn.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    ).fetchone()[0]

    print(f"{table:<25} {count:>8} rows")

conn.close()
