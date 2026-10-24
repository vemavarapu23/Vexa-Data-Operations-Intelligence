
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vexa.db"


# Create SQLite database and audit history table
def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS audit_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                finding_id TEXT,
                record_id TEXT,
                reviewer TEXT,
                details TEXT
            )
        """)
        connection.commit()


# Save a review, correction, or deletion permanently
def save_audit_action(
    timestamp,
    action,
    finding_id,
    record_id,
    reviewer,
    details
):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO audit_history
            (
                timestamp,
                action,
                finding_id,
                record_id,
                reviewer,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                action,
                finding_id,
                record_id,
                reviewer,
                details
            )
        )
        connection.commit()


# Run directly to initialize database
if __name__ == "__main__":
    initialize_database()
    print("Vexa SQLite database created successfully!")
