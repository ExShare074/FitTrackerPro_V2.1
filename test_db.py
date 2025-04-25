import sqlite3
db_path = r"C:\Users\deadm\Documents\GitHub\FitTrackerPro_V2.1\data\workouts.db"
print(f"Connecting to: {db_path}")
try:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()
    print("Database connection successful")
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")