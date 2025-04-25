import sqlite3
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path):
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            print(f"Database path: {os.path.abspath(db_path)}")
            self.conn = sqlite3.connect(db_path)
            self.create_tables()
        except sqlite3.OperationalError as e:
            raise Exception(f"Failed to connect to database: {e}")

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS cycles (
                    user_id INTEGER,
                    weeks INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS weights (
                    user_id INTEGER,
                    exercise TEXT,
                    weight REAL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

    def add_user(self, name):
        with self.conn:
            self.conn.execute("INSERT INTO users (name) VALUES (?)", (name,))

    def get_users(self):
        return self.conn.execute("SELECT id, name FROM users").fetchall()

    def start_cycle(self, user_id, weeks, start_date, end_date):
        with self.conn:
            self.conn.execute("DELETE FROM cycles WHERE user_id = ?", (user_id,))
            self.conn.execute("INSERT INTO cycles (user_id, weeks, start_date, end_date) VALUES (?, ?, ?, ?)",
                             (user_id, weeks, start_date, end_date))

    def get_user_cycle(self, user_id):
        return self.conn.execute("SELECT * FROM cycles WHERE user_id = ?", (user_id,)).fetchone()

    def get_user_weight(self, user_id, exercise):
        result = self.conn.execute("SELECT weight FROM weights WHERE user_id = ? AND exercise = ?",
                                  (user_id, exercise)).fetchone()
        return result[0] if result else None