from pathlib import Path
import sqlite3

DB_PATH = Path(
    r"C:\Users\vansh\OneDrive\Desktop\Mutual Fund Analytics\sql\mutual_fund.db"
)

print("Database exists:", DB_PATH.exists())
print("Database path:", DB_PATH)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("\nDATABASE TABLES")
print("=" * 50)

for (table,) in tables:
    cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
    count = cursor.fetchone()[0]
    print(f"{table:<35} {count:>8} rows")

conn.close()