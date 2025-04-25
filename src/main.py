import os
import sys

from PyQt5.QtWidgets import QApplication

# Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ui import FitnessTrackerApp
from src.database import Database

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database(os.path.join("data", "workouts.db"))
    window = FitnessTrackerApp(db)
    window.show()
    sys.exit(app.exec_())