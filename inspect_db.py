import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "nifty100.db"

print("Database path:")
print(DB_PATH)

print("\nDatabase exists:", DB_PATH.exists())

if not DB_PATH.exists():
    print("\nERROR: nifty100.db was not found!")
    input("\nPress Enter to exit...")
    raise SystemExit

try:
    conn = sqlite3.connect(DB_PATH)

    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name != 'sqlite_sequence'
        ORDER BY name;
    """).fetchall()

    print("\n" + "=" * 60)
    print("NIFTY100 DATABASE")
    print("=" * 60)

    if not tables:
        print("No tables found!")
    else:
        for (table,) in tables:
            count = conn.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]

            print(f"{table:<30} {count:>8,} rows")

    print("=" * 60)

    conn.close()

except Exception as e:
    print("\nERROR:")
    print(type(e).__name__, e)

input("\nPress Enter to exit...")