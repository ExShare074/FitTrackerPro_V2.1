import sys
import traceback
from PyQt5.QtWidgets import QApplication
from src.database import Database
from src.ui import FitnessTrackerApp

if __name__ == "__main__":
    if not hasattr(sys, '_fittrackerpro_running'):
        sys._fittrackerpro_running = True
    else:
        print("Already running, exiting")
        sys.exit(0)

    try:
        print("Starting QApplication")
        app = QApplication(sys.argv)
        db_path = r"C:\Users\deadm\Documents\GitHub\FitTrackerPro_V2.1\data\workouts.db"
        print(f"Database path: {db_path}")
        print("Initializing Database")
        db = Database(db_path)
        print("Initializing FitnessTrackerApp")
        window = FitnessTrackerApp(db)
        print("Showing window")
        window.show()
        print("Entering event loop")
        sys.exit(app.exec_())
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))
            f.write("\n")
            f.write(traceback.format_exc())
        raise