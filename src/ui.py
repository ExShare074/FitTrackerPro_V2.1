from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QDialog, QCalendarWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta
from src.workout_plan import WorkoutPlan
import logging

# Setup logging
logging.basicConfig(filename='fittracker.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FitnessTrackerApp(QMainWindow):
    translations = {
        "en": {
            "FitTracker Pro": "FitTracker Pro",
            "User:": "User:",
            "Add User": "Add User",
            "Cycle:": "Cycle:",
            "Start Cycle": "Start Cycle",
            "Complete Workout": "Complete Workout",
            "Workout saved!": "Workout saved!",
            "View History": "View History",
            "Workout History": "Workout History",
            "Exercise": "Exercise",
            "Sets": "Sets",
            "Reps": "Reps",
            "Weight (kg)": "Weight (kg)",
            "Language:": "Language:",
            "Training Split:": "Training Split:",
            "5-day Split": "5-day Split",
            "3-day Split": "3-day Split",
            "Error": "Error",
            "Select a user first!": "Select a user first!",
            "8 weeks": "8 weeks",
            "10 weeks": "10 weeks",
            "12 weeks": "12 weeks",
            "Muscle Group": "Muscle Group",
            "Date": "Date",
            "Chest": "Chest",
            "Back": "Back",
            "Legs": "Legs",
            "Shoulders": "Shoulders",
            "Biceps": "Biceps",
            "Triceps": "Triceps",
            "Bench Press": "Bench Press",
            "Dumbbell Press": "Dumbbell Press",
            "Incline Dumbbell Press": "Incline Dumbbell Press",
            "Deadlift": "Deadlift",
            "Bent-over Row": "Bent-over Row",
            "Pull-up": "Pull-up",
            "Squat": "Squat",
            "Leg Press": "Leg Press",
            "Lunges": "Lunges",
            "Overhead Barbell Press": "Overhead Barbell Press",
            "Dumbbell Lateral Raise": "Dumbbell Lateral Raise",
            "Barbell Shrug": "Barbell Shrug",
            "EZ-Bar Curl": "EZ-Bar Curl",
            "Tricep Dip": "Tricep Dip",
            "Hammer Curl": "Hammer Curl",
            "Hammer Strength Chest Press": "Hammer Strength Chest Press",
            "Cable Crossover": "Cable Crossover",
            "Seated Cable Row": "Seated Cable Row",
            "Cable Pullover": "Cable Pullover",
            "Lying Leg Curl": "Lying Leg Curl",
            "Leg Extension": "Leg Extension",
            "Machine Shoulder Press": "Machine Shoulder Press",
            "Machine Lateral Raise": "Machine Lateral Raise",
            "Cable Pushdown": "Cable Pushdown",
            "Machine Curl": "Machine Curl",
            "Machine Tricep Extension": "Machine Tricep Extension",
            "No workouts available": "No workouts available for this week."
        },
        "ru": {
            "FitTracker Pro": "FitTracker Pro",
            "User:": "Пользователь:",
            "Add User": "Добавить пользователя",
            "Cycle:": "Цикл:",
            "Start Cycle": "Начать цикл",
            "Complete Workout": "Завершить тренировку",
            "Workout saved!": "Тренировка сохранена!",
            "View History": "Просмотреть историю",
            "Workout History": "История тренировок",
            "Exercise": "Упражнение",
            "Sets": "Подходы",
            "Reps": "Повторения",
            "Weight (kg)": "Вес (кг)",
            "Language:": "Язык:",
            "Training Split:": "Тренировочный сплит:",
            "5-day Split": "5-дневный сплит",
            "3-day Split": "3-дневный сплит",
            "Error": "Ошибка",
            "Select a user first!": "Сначала выберите пользователя!",
            "8 weeks": "8 недель",
            "10 weeks": "10 недель",
            "12 weeks": "12 недель",
            "Muscle Group": "Мышечная группа",
            "Date": "Дата",
            "Chest": "Грудь",
            "Back": "Спина",
            "Legs": "Ноги",
            "Shoulders": "Плечи",
            "Biceps": "Бицепсы",
            "Triceps": "Трицепсы",
            "Bench Press": "Жим лежа",
            "Dumbbell Press": "Жим гантелей",
            "Incline Dumbbell Press": "Жим гантелей на наклонной скамье",
            "Deadlift": "Становая тяга",
            "Bent-over Row": "Тяга штанги в наклоне",
            "Pull-up": "Подтягивания",
            "Squat": "Приседания",
            "Leg Press": "Жим ногами",
            "Lunges": "Выпады",
            "Overhead Barbell Press": "Жим штанги над головой",
            "Dumbbell Lateral Raise": "Подъем гантелей в стороны",
            "Barbell Shrug": "Шраги со штангой",
            "EZ-Bar Curl": "Сгибания рук с EZ-штангой",
            "Tricep Dip": "Отжимания на брусьях",
            "Hammer Curl": "Сгибания рук с молотом",
            "Hammer Strength Chest Press": "Жим в тренажере Hammer",
            "Cable Crossover": "Сведение рук в кроссовере",
            "Seated Cable Row": "Тяга блока сидя",
            "Cable Pullover": "Пулловер на блоке",
            "Lying Leg Curl": "Сгибания ног лежа",
            "Leg Extension": "Разгибания ног",
            "Machine Shoulder Press": "Жим в тренажере для плеч",
            "Machine Lateral Raise": "Боковые подъемы в тренажере",
            "Cable Pushdown": "Разгибания на трицепс с канатом",
            "Machine Curl": "Сгибания на бицепс в тренажере",
            "Machine Tricep Extension": "Разгибания на трицепс в тренажере",
            "No workouts available": "Нет доступных тренировок для этой недели."
        }
    }

    def __init__(self, db):
        super().__init__()
        self.db = db
        lang = self.db.conn.execute("SELECT value FROM settings WHERE key = 'language'").fetchone()
        self.current_language = lang[0] if lang else "en"
        self.control_layout = None
        self.setWindowTitle(self.tr("FitTracker Pro"))
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.load_users()
        last_user = self.db.conn.execute("SELECT value FROM settings WHERE key = 'last_user'").fetchone()
        if last_user:
            for index in range(self.user_combo.count()):
                if self.user_combo.itemData(index) == int(last_user[0]):
                    self.user_combo.setCurrentIndex(index)
                    break
        self.language_combo.setCurrentText("Русский" if self.current_language == "ru" else "English")

    def tr(self, text):
        return self.translations[self.current_language].get(text, text)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E63946;
                border-radius: 5px;
                background-color: #2C2F33;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #1DB954, stop: 1 #127B3C);
                border-radius: 3px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Control Panel
        self.control_layout = QHBoxLayout()
        self.control_layout.setSpacing(10)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Русский"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                padding: 8px;
                color: #2C2F33;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #F1FAEE;
            }
        """)
        self.control_layout.addWidget(QLabel(self.tr("Language:")))
        self.control_layout.addWidget(self.language_combo)

        self.training_days_combo = QComboBox()
        self.training_days_combo.addItem(self.tr("5-day Split"), 5)
        self.training_days_combo.addItem(self.tr("3-day Split"), 3)
        self.training_days_combo.currentIndexChanged.connect(self.load_user_data)
        self.training_days_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                padding: 8px;
                color: #2C2F33;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #F1FAEE;
            }
        """)
        self.control_layout.addWidget(QLabel(self.tr("Training Split:")))
        self.control_layout.addWidget(self.training_days_combo)

        self.user_combo = QComboBox()
        self.user_combo.currentIndexChanged.connect(self.load_user_data)
        self.user_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                padding: 8px;
                color: #2C2F33;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #F1FAEE;
            }
        """)
        self.control_layout.addWidget(QLabel(self.tr("User:")))
        self.control_layout.addWidget(self.user_combo)

        add_user_btn = QPushButton(self.tr("Add User"))
        add_user_btn.clicked.connect(self.add_user)
        add_user_btn.setIcon(QIcon("resources/user.png"))
        self.control_layout.addWidget(add_user_btn)

        self.cycle_combo = QComboBox()
        self.cycle_combo.addItems([self.tr("8 weeks"), self.tr("10 weeks"), self.tr("12 weeks")])
        self.cycle_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                padding: 8px;
                color: #2C2F33;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #F1FAEE;
            }
        """)
        self.control_layout.addWidget(QLabel(self.tr("Cycle:")))
        self.control_layout.addWidget(self.cycle_combo)

        start_cycle_btn = QPushButton(self.tr("Start Cycle"))
        start_cycle_btn.clicked.connect(self.start_cycle)
        start_cycle_btn.setIcon(QIcon("resources/cycle.png"))
        self.control_layout.addWidget(start_cycle_btn)

        main_layout.addLayout(self.control_layout)

        # Workout Table
        self.workout_table = QTableWidget()
        self.workout_table.setColumnCount(4)
        self.workout_table.setHorizontalHeaderLabels([
            self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
        ])
        self.workout_table.itemChanged.connect(self.update_weight)
        self.workout_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                gridline-color: #E63946;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2C2F33;
            }
            QTableWidget::item:nth-child(even) {
                background-color: #F1FAEE;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #FFFFFF;
            }
            QTableWidget::item:selected {
                background-color: #E63946;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #E63946;
                color: #FFFFFF;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
        """)
        main_layout.addWidget(self.workout_table)

        # Action Buttons
        complete_workout_btn = QPushButton(self.tr("Complete Workout"))
        complete_workout_btn.clicked.connect(self.complete_workout)
        complete_workout_btn.setIcon(QIcon("resources/dumbbell.png"))
        main_layout.addWidget(complete_workout_btn)

        history_btn = QPushButton(self.tr("View History"))
        history_btn.clicked.connect(self.view_history)
        history_btn.setIcon(QIcon("resources/calendar.png"))
        main_layout.addWidget(history_btn)

        # Global Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #2C2F33, stop: 1 #4A4E54);
            }
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton {
                background-color: #E63946;
                color: #FFFFFF;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Roboto', sans-serif;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #F1FAEE;
                color: #E63946;
            }
        """)

    def change_language(self):
        language = self.language_combo.currentText()
        self.current_language = "ru" if language == "Русский" else "en"
        self.db.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                            ("language", self.current_language))
        self.db.conn.commit()
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("FitTracker Pro"))
        self.workout_table.setHorizontalHeaderLabels([
            self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
        ])
        for i in range(self.control_layout.count()):
            item = self.control_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if isinstance(widget, QLabel):
                current_text = widget.text()
                for key, value in self.translations["en"].items():
                    if current_text == value or current_text == self.translations["ru"].get(key):
                        widget.setText(self.tr(key))
                        break
            elif isinstance(widget, QPushButton):
                current_text = widget.text()
                for key, value in self.translations["en"].items():
                    if current_text == value or current_text == self.translations["ru"].get(key):
                        widget.setText(self.tr(key))
                        break
        current_index = self.cycle_combo.currentIndex()
        self.cycle_combo.clear()
        self.cycle_combo.addItems([self.tr("8 weeks"), self.tr("10 weeks"), self.tr("12 weeks")])
        self.cycle_combo.setCurrentIndex(current_index if current_index >= 0 else 0)
        current_days_index = self.training_days_combo.currentIndex()
        self.training_days_combo.clear()
        self.training_days_combo.addItem(self.tr("5-day Split"), 5)
        self.training_days_combo.addItem(self.tr("3-day Split"), 3)
        self.training_days_combo.setCurrentIndex(current_days_index if current_days_index >= 0 else 0)
        for row in range(self.workout_table.rowCount()):
            exercise_item = self.workout_table.item(row, 0)
            if exercise_item:
                current_exercise = exercise_item.text().replace(" (FST-7)", "")
                for key, value in self.translations["en"].items():
                    if current_exercise == value or current_exercise == self.translations["ru"].get(key):
                        exercise_item.setText(self.tr(key) + (" (FST-7)" if self.workout_table.item(row, 0).data(Qt.UserRole) else ""))
                        break

    def load_users(self):
        self.user_combo.clear()
        users = self.db.get_users()
        for user in users:
            self.user_combo.addItem(user[1], user[0])
        if users:
            self.load_user_data()

    def add_user(self):
        name, ok = QInputDialog.getText(self, self.tr("Add User"), self.tr("Add User"))
        if ok and name:
            self.db.add_user(name)
            self.load_users()

    def start_cycle(self):
        user_id = self.user_combo.currentData()
        if not user_id:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Select a user first!"))
            return
        cycle_weeks = int(self.cycle_combo.currentText().split()[0])
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=cycle_weeks)
        try:
            self.db.start_cycle(user_id, cycle_weeks, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            logging.info(f"Cycle started for user {user_id}: {cycle_weeks} weeks, start {start_date}, end {end_date}")
            self.load_user_data()
        except Exception as e:
            logging.error(f"Failed to start cycle: {str(e)}")
            QMessageBox.critical(self, self.tr("Error"), f"Failed to start cycle: {str(e)}")

    def load_user_data(self):
        user_id = self.user_combo.currentData()
        if user_id:
            try:
                self.db.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                                    ("last_user", str(user_id)))
                self.db.conn.commit()
                logging.info(f"Saved last_user: {user_id}")
            except Exception as e:
                logging.error(f"Failed to save last_user: {str(e)}")
        if not user_id:
            logging.warning("No user selected")
            return
        cycle = self.db.get_user_cycle(user_id)
        logging.info(f"Cycle for user {user_id}: {cycle}")
        if cycle:
            start_date = datetime.strptime(cycle[2], "%Y-%m-%d")
            end_date = datetime.strptime(cycle[3], "%Y-%m-%d")
            total_days = (end_date - start_date).days
            days_passed = (datetime.now() - start_date).days
            progress = min(100, (days_passed / total_days) * 100)
            self.progress_bar.setValue(int(progress))
            self.load_workouts(user_id, cycle[1])
        else:
            logging.warning("No cycle found, clearing workout table")
            self.progress_bar.setValue(0)
            self.workout_table.setRowCount(0)
            self.workout_table.setRowCount(1)
            self.workout_table.setItem(0, 0, QTableWidgetItem(self.tr("No workouts available")))
            self.workout_table.setItem(0, 1, QTableWidgetItem(""))
            self.workout_table.setItem(0, 2, QTableWidgetItem(""))
            self.workout_table.setItem(0, 3, QTableWidgetItem(""))

    def load_workouts(self, user_id, cycle_weeks):
        try:
            cycle = self.db.get_user_cycle(user_id)
            if not cycle:
                logging.error("No cycle found in load_workouts")
                self.workout_table.setRowCount(1)
                self.workout_table.setItem(0, 0, QTableWidgetItem(self.tr("No workouts available")))
                self.workout_table.setItem(0, 1, QTableWidgetItem(""))
                self.workout_table.setItem(0, 2, QTableWidgetItem(""))
                self.workout_table.setItem(0, 3, QTableWidgetItem(""))
                return
            current_week = min((datetime.now() - datetime.strptime(cycle[2], "%Y-%m-%d")).days // 7 + 1, cycle_weeks)
            training_days = self.training_days_combo.currentData()
            logging.info(f"Loading workouts for user {user_id}, week {current_week}, {training_days}-day split")
            plan = WorkoutPlan(cycle_weeks, current_week, training_days)
            workouts = plan.get_workouts(user_id, self.db)
            logging.info(f"Workouts retrieved: {workouts}")
            if not workouts:
                logging.warning("No workouts returned by WorkoutPlan")
                self.workout_table.setRowCount(1)
                self.workout_table.setItem(0, 0, QTableWidgetItem(self.tr("No workouts available")))
                self.workout_table.setItem(0, 1, QTableWidgetItem(""))
                self.workout_table.setItem(0, 2, QTableWidgetItem(""))
                self.workout_table.setItem(0, 3, QTableWidgetItem(""))
                return
            self.workout_table.setRowCount(len(workouts))
            for i, workout in enumerate(workouts):
                exercise_item = QTableWidgetItem(self.tr(workout["exercise"]) + (" (FST-7)" if workout.get("fst7") else ""))
                exercise_item.setData(Qt.UserRole, workout.get("fst7", False))
                exercise_item.setFlags(exercise_item.flags() & ~Qt.ItemIsEditable)
                self.workout_table.setItem(i, 0, exercise_item)
                self.workout_table.setItem(i, 1, QTableWidgetItem(str(workout["sets"])))
                self.workout_table.setItem(i, 2, QTableWidgetItem(str(workout["reps"])))
                weight = workout["suggested_weight"]
                weight_item = QTableWidgetItem(str(weight))
                weight_item.setFlags(weight_item.flags() | Qt.ItemIsEditable)
                self.workout_table.setItem(i, 3, weight_item)
            self.workout_table.resizeColumnsToContents()
        except Exception as e:
            logging.error(f"Error in load_workouts: {str(e)}")
            self.workout_table.setRowCount(1)
            self.workout_table.setItem(0, 0, QTableWidgetItem(self.tr("No workouts available")))
            self.workout_table.setItem(0, 1, QTableWidgetItem(""))
            self.workout_table.setItem(0, 2, QTableWidgetItem(""))
            self.workout_table.setItem(0, 3, QTableWidgetItem(""))

    def update_weight(self, item):
        if item.column() != 3:
            return
        user_id = self.user_combo.currentData()
        if not user_id:
            return
        row = item.row()
        exercise = self.workout_table.item(row, 0).text().replace(" (FST-7)", "")
        try:
            weight = float(item.text())
            self.db.conn.execute("INSERT OR REPLACE INTO weights (user_id, exercise, weight) VALUES (?, ?, ?)",
                                (user_id, exercise, weight))
            self.db.conn.commit()
        except ValueError:
            QMessageBox.warning(self, self.tr("Error"), "Please enter a valid weight!")
            item.setText(str(self.db.get_user_weight(user_id, exercise) or 0))

    def complete_workout(self):
        user_id = self.user_combo.currentData()
        if not user_id:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Select a user first!"))
            return
        for row in range(self.workout_table.rowCount()):
            exercise_item = self.workout_table.item(row, 0)
            if not exercise_item or "No workouts available" in exercise_item.text():
                continue
            exercise = exercise_item.text().replace(" (FST-7)", "")
            sets = int(self.workout_table.item(row, 1).text())
            reps = self.workout_table.item(row, 2).text().split('-')[-1]
            try:
                weight = float(self.workout_table.item(row, 3).text())
            except ValueError:
                QMessageBox.warning(self, self.tr("Error"), f"Invalid weight in row {row + 1}")
                return
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.save_workout(user_id, exercise, sets, int(reps), weight, date)
            self.db.conn.execute("INSERT OR REPLACE INTO weights (user_id, exercise, weight) VALUES (?, ?, ?)",
                                (user_id, exercise, weight))
            self.db.conn.commit()
        QMessageBox.information(self, self.tr("Success"), self.tr("Workout saved!"))

    def view_history(self):
        user_id = self.user_combo.currentData()
        if not user_id:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Select a user first!"))
            return
        dialog = HistoryDialog(self.db, user_id, self.current_language, self)
        dialog.exec_()

class HistoryDialog(QDialog):
    def __init__(self, db, user_id, language, parent=None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.language = language
        self.translations = FitnessTrackerApp.translations
        self.setWindowTitle(self.tr("Workout History"))
        self.setGeometry(200, 200, 800, 600)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.load_workouts_for_date)
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #E63946;
                selection-color: #FFFFFF;
            }
        """)
        layout.addWidget(self.calendar)

        # Workout Tree
        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels([
            self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
        ])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 100)
        self.tree.setColumnWidth(2, 100)
        self.tree.setColumnWidth(3, 100)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #FFFFFF;
                border: 1px solid #E63946;
                border-radius: 5px;
                font-size: 14px;
            }
            QTreeWidget::item {
                padding: 8px;
                color: #2C2F33;
            }
            QTreeWidget::item:nth-child(even) {
                background-color: #F1FAEE;
            }
            QTreeWidget::item:nth-child(odd) {
                background-color: #FFFFFF;
            }
            QTreeWidget::item:selected {
                background-color: #E63946;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #E63946;
                color: #FFFFFF;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
        """)
        layout.addWidget(self.tree)

        # Highlight completed workout dates
        workouts = self.db.conn.execute("SELECT DISTINCT date FROM workouts WHERE user_id = ?", (self.user_id,)).fetchall()
        for workout in workouts:
            date = datetime.strptime(workout[0], "%Y-%m-%d").date()
            format = self.calendar.dateTextFormat(date)
            format.setBackground(Qt.green)
            self.calendar.setDateTextFormat(date, format)

        # Dialog Styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #2C2F33, stop: 1 #4A4E54);
            }
        """)

    def tr(self, text):
        return self.translations[self.language].get(text, text)

    def load_workouts_for_date(self, qdate):
        self.tree.clear()
        date_str = qdate.toString("yyyy-MM-dd")
        workouts = self.db.conn.execute(
            "SELECT exercise, sets, reps, weight FROM workouts WHERE user_id = ? AND date = ?",
            (self.user_id, date_str)
        ).fetchall()
        if not workouts:
            return

        # Group workouts by muscle group
        muscle_groups = {
            "Chest": ["Bench Press", "Incline Dumbbell Press", "Hammer Strength Chest Press", "Cable Crossover"],
            "Back": ["Bent-over Row", "Pull-up", "Seated Cable Row", "Cable Pullover"],
            "Legs": ["Squat", "Leg Press", "Lying Leg Curl", "Leg Extension"],
            "Shoulders": ["Overhead Barbell Press", "Dumbbell Lateral Raise", "Machine Shoulder Press", "Machine Lateral Raise"],
            "Biceps": ["EZ-Bar Curl", "Hammer Curl", "Machine Curl"],
            "Triceps": ["Cable Pushdown", "Tricep Dip", "Machine Tricep Extension"]
        }
        workouts_by_group = {}
        for exercise, sets, reps, weight in workouts:
            for group, exercises in muscle_groups.items():
                if exercise in exercises:
                    if group not in workouts_by_group:
                        workouts_by_group[group] = []
                    workouts_by_group[group].append((exercise, sets, reps, weight))
                    break

        # Populate tree with muscle groups and workouts
        for group, group_workouts in workouts_by_group.items():
            group_item = QTreeWidgetItem(self.tree, [self.tr(group), "", "", ""])
            group_item.setFlags(group_item.flags() & ~Qt.ItemIsSelectable)
            group_item.setBackground(0, Qt.lightGray)
            group_item.setBackground(1, Qt.lightGray)
            group_item.setBackground(2, Qt.lightGray)
            group_item.setBackground(3, Qt.lightGray)
            group_item.setFont(0, self.tree.font())
            group_item.setFont(0, self.tree.font().setBold(True))
            for i, (exercise, sets, reps, weight) in enumerate(group_workouts):
                workout_item = QTreeWidgetItem(group_item, [
                    self.tr(exercise), str(sets), str(reps), str(weight)
                ])
                workout_item.setTextAlignment(1, Qt.AlignCenter)
                workout_item.setTextAlignment(2, Qt.AlignCenter)
                workout_item.setTextAlignment(3, Qt.AlignCenter)
                if i % 2 == 0:
                    workout_item.setBackground(0, Qt.white)
                    workout_item.setBackground(1, Qt.white)
                    workout_item.setBackground(2, Qt.white)
                    workout_item.setBackground(3, Qt.white)
                else:
                    workout_item.setBackground(0, Qt.lightGray)
                    workout_item.setBackground(1, Qt.lightGray)
                    workout_item.setBackground(2, Qt.lightGray)
                    workout_item.setBackground(3, Qt.lightGray)
        self.tree.expandAll()