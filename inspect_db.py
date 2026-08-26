import sqlite3
from pathlib import Path

DB_PATH = Path(
    r"C:\Users\vansh\OneDrive\Desktop\Mutual Fund Analytics\sql\mutual_fund.db"
)

conn = sqlite3.connect(DB_PATH)

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
]

for table in tables:
    print("\n" + "=" * 70)
    print(table.upper())
    print("=" * 70)

    try:
        rows = conn.execute(
            f'PRAGMA table_info("{table}")'
        ).fetchall()

        for row in rows:
            print(f"{row[1]:35} {row[2]}")

        count = conn.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]

        print(f"\nRows: {count}")

    except sqlite3.Error as e:
        print(f"ERROR: {e}")

conn.close()