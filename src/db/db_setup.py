import sqlite3
import csv
import os
from pathlib import Path

def initialize_db():
    # Go two levels up from the script to get the actual project root
    project_root = Path(__file__).resolve().parents[2]

    # Build paths relative to the project root
    db_path = project_root / 'src' / 'db' / 'database.db'
    csv_path = project_root / 'data' / 'financial_metrics.csv'

    print(f"Project root detected as: {project_root}")
    print(f"Connecting to database at: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return

    cursor = conn.cursor()

    print("Creating table 'financial_metrics' if it doesn't exist...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            company TEXT NOT NULL,
            industry TEXT NOT NULL,
            best_metric TEXT NOT NULL,
            why TEXT
        )
    ''')

    print("Checking if table is empty...")
    cursor.execute('SELECT COUNT(*) FROM financial_metrics')
    count = cursor.fetchone()[0]
    print(f"Row count in 'financial_metrics': {count}")

    if count == 0:
        print("Table is empty.")
        if csv_path.exists():
            print(f"CSV file found at: {csv_path}")
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='|')
                # Add this line to print the headers
                print("CSV headers:", reader.fieldnames)

                rows_inserted = 0
                for row in reader:
                    cursor.execute('''
                        INSERT INTO financial_metrics (ticker, company, industry, best_metric, why)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (row['ticker'], row['company'], row['industry'], row['best_metric'], row['why']))
                    rows_inserted += 1
                print(f"Inserted {rows_inserted} rows from CSV into the database.")
        else:
            print(f"CSV file not found at: {csv_path}")
    else:
        print("Table is not empty. Skipping CSV load.")

    conn.commit()
    conn.close()
    print("Database connection closed.")
