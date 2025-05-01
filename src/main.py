import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication
import logging

# Setup logging
logging.basicConfig(filename='fittracker.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Adjust module path for packaged executable
if getattr(sys, '_MEIPASS', None):
    # Running as packaged executable
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    base_path = sys._MEIPASS
else:
    # Running in development environment
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from ui import FitnessTrackerApp

if __name__ == "__main__":
    if not hasattr(sys, '_fittrackerpro_running'):
        sys._fittrackerpro_running = True
    else:
        logging.info("Already running, exiting")
        sys.exit(0)

    try:
        logging.info("Starting QApplication")
        app = QApplication(sys.argv)
        # Set database path relative to base_path
        db_path = os.path.join(base_path, "data", "workouts.db")
        logging.info(f"Database path: {db_path}, exists: {os.path.exists(db_path)}")
        logging.info("Initializing Database")
        db = Database(db_path)
        logging.info("Initializing FitnessTrackerApp")
        window = FitnessTrackerApp(db)
        logging.info("Showing window")
        window.show()
        logging.info("Entering event loop")
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        with open("error.log", "w") as f:
            f.write(str(e))
            f.write("\n")
            f.write(traceback.format_exc())
        raise