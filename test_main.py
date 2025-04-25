import sqlite3
import sys

if __name__ == "__main__":
    db_path = r"C:\Users\deadm\Documents\GitHub\FitTrackerPro_V2.1\data\workouts.db"
    print(f"Database path: {db_path}")
    try:
        print("Connecting to database")
        conn = sqlite3.connect(db_path, timeout=10)
        conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()
        print("Database operation successful")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)