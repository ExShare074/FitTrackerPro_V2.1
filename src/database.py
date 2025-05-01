import sqlite3
import os

class Database:
    def __init__(self, db_path):
        print(f"Database path exists: {os.path.exists(db_path)}")
        try:
            self.conn = sqlite3.connect(db_path, timeout=10)
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.create_tables()
            self.migrate_schema()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in Database.__init__: {e}")
            raise

    def create_tables(self):
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT NOT NULL,
                                 telegram_id INTEGER UNIQUE)''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS cycles
                                (user_id INTEGER,
                                 cycle_weeks INTEGER,
                                 start_date TEXT,
                                 end_date TEXT,
                                 FOREIGN KEY(user_id) REFERENCES users(id))''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weights
                                (user_id INTEGER,
                                 exercise TEXT,
                                 weight REAL,
                                 FOREIGN KEY(user_id) REFERENCES users(id))''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS settings
                                (key TEXT PRIMARY KEY,
                                 value TEXT)''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS workouts
                                (user_id INTEGER,
                                 exercise TEXT,
                                 sets INTEGER,
                                 reps INTEGER,
                                 weight REAL,
                                 date TEXT,
                                 FOREIGN KEY(user_id) REFERENCES users(id))''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in create_tables: {e}")
            raise

    def migrate_schema(self):
        try:
            # Проверяем, существует ли столбец telegram_id в таблице users
            cursor = self.conn.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'telegram_id' not in columns:
                print("Adding telegram_id column to users table")
                self.conn.execute("ALTER TABLE users ADD COLUMN telegram_id INTEGER UNIQUE")
                self.conn.commit()
                print("telegram_id column added successfully")
        except sqlite3.Error as e:
            print(f"Schema migration error: {e}")
            raise

    def add_user(self, name, telegram_id):
        try:
            cursor = self.conn.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
            if cursor.fetchone():
                return  # Пользователь уже существует
            self.conn.execute("INSERT INTO users (name, telegram_id) VALUES (?, ?)", (name, telegram_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            raise

    def get_user_id(self, telegram_id):
        try:
            cursor = self.conn.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error getting user id: {e}")
            raise

    def get_users(self):
        try:
            cursor = self.conn.execute("SELECT * FROM users")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting users: {e}")
            raise

    def start_cycle(self, user_id, cycle_weeks, start_date, end_date):
        try:
            self.conn.execute("INSERT INTO cycles (user_id, cycle_weeks, start_date, end_date) VALUES (?, ?, ?, ?)",
                             (user_id, cycle_weeks, start_date, end_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error starting cycle: {e}")
            raise

    def get_user_cycle(self, user_id):
        try:
            cursor = self.conn.execute("SELECT * FROM cycles WHERE user_id = ? ORDER BY start_date DESC LIMIT 1", (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user cycle: {e}")
            raise

    def get_user_weight(self, user_id, exercise):
        try:
            cursor = self.conn.execute("SELECT weight FROM weights WHERE user_id = ? AND exercise = ?", (user_id, exercise))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error getting user weight: {e}")
            raise

    def save_workout(self, user_id, exercise, sets, reps, weight, date):
        try:
            self.conn.execute("INSERT INTO workouts (user_id, exercise, sets, reps, weight, date) VALUES (?, ?, ?, ?, ?, ?)",
                             (user_id, exercise, sets, reps, weight, date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving workout: {e}")
            raise

    def get_workouts(self, user_id):
        try:
            cursor = self.conn.execute("SELECT exercise, sets, reps, weight, date FROM workouts WHERE user_id = ?", (user_id,))
            return [{"exercise": row[0], "sets": row[1], "reps": row[2], "weight": row[3], "date": row[4]} for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error getting workouts: {e}")
            raise