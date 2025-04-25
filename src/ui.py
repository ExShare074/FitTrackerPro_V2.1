from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, \
    QProgressBar, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
from src.workout_plan import WorkoutPlan


class FitnessTrackerApp(QMainWindow):
    translations = {
        "en": {
            "Fitness Tracker FST-8": "Fitness Tracker FST-8",
            "User:": "User:",
            "Add User": "Add User",
            "Cycle:": "Cycle:",
            "Start Cycle": "Start Cycle",
            "Exercise": "Exercise",
            "Sets": "Sets",
            "Reps": "Reps",
            "Weight (kg)": "Weight (kg)",
            "Language:": "Language:",
            "Error": "Error",
            "Select a user first!": "Select a user first!",
            # Переводы длительности цикла
            "8 weeks": "8 weeks",
            "10 weeks": "10 weeks",
            "12 weeks": "12 weeks",
            # Переводы упражнений
            "Bench Press": "Bench Press",
            "Dumbbell Press": "Dumbbell Press",
            "Incline Bench Press": "Incline Bench Press",
            "Deadlift": "Deadlift",
            "Bent-over Row": "Bent-over Row",
            "Pull-up": "Pull-up",
            "Squat": "Squat",
            "Leg Press": "Leg Press",
            "Lunges": "Lunges",
            "Overhead Press": "Overhead Press",
            "Dumbbell Raise": "Dumbbell Raise",
            "Barbell Shrug": "Barbell Shrug",
            "Bicep Curl": "Bicep Curl",
            "Tricep Dip": "Tricep Dip",
            "Hammer Curl": "Hammer Curl"
        },
        "ru": {
            "Fitness Tracker FST-8": "Фитнес-трекер FST-8",
            "User:": "Пользователь:",
            "Add User": "Добавить пользователя",
            "Cycle:": "Цикл:",
            "Start Cycle": "Начать цикл",
            "Exercise": "Упражнение",
            "Sets": "Подходы",
            "Reps": "Повторения",
            "Weight (kg)": "Вес (кг)",
            "Language:": "Язык:",
            "Error": "Ошибка",
            "Select a user first!": "Сначала выберите пользователя!",
            # Переводы длительности цикла
            "8 weeks": "8 недель",
            "10 weeks": "10 недель",
            "12 weeks": "12 недель",
            # Переводы упражнений
            "Bench Press": "Жим лежа",
            "Dumbbell Press": "Жим гантелей",
            "Incline Bench Press": "Жим лежа на наклонной скамье",
            "Deadlift": "Становая тяга",
            "Bent-over Row": "Тяга штанги в наклоне",
            "Pull-up": "Подтягивания",
            "Squat": "Приседания",
            "Leg Press": "Жим ногами",
            "Lunges": "Выпады",
            "Overhead Press": "Жим над головой",
            "Dumbbell Raise": "Подъем гантелей",
            "Barbell Shrug": "Шраги со штангой",
            "Bicep Curl": "Сгибание рук со штангой",
            "Tricep Dip": "Отжимания на брусьях",
            "Hammer Curl": "Молотковый сгиб"
        }
    }

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_language = "en"  # Язык по умолчанию
        self.control_layout = None  # Сохраняем layout для доступа в retranslate_ui
        self.setWindowTitle(self.tr("Fitness Tracker FST-8"))
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.load_users()

    def tr(self, text):
        return self.translations[self.current_language].get(text, text)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar {border: 1px solid black; background-color: black;}"
                                        "QProgressBar::chunk {background-color: green;}")
        main_layout.addWidget(self.progress_bar)

        self.control_layout = QHBoxLayout()

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Русский"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.control_layout.addWidget(QLabel(self.tr("Language:")))
        self.control_layout.addWidget(self.language_combo)

        self.user_combo = QComboBox()
        self.user_combo.currentIndexChanged.connect(self.load_user_data)
        self.control_layout.addWidget(QLabel(self.tr("User:")))
        self.control_layout.addWidget(self.user_combo)
        add_user_btn = QPushButton(self.tr("Add User"))
        add_user_btn.clicked.connect(self.add_user)
        self.control_layout.addWidget(add_user_btn)
        self.cycle_combo = QComboBox()
        self.cycle_combo.addItems([self.tr("8 weeks"), self.tr("10 weeks"), self.tr("12 weeks")])
        self.control_layout.addWidget(QLabel(self.tr("Cycle:")))
        self.control_layout.addWidget(self.cycle_combo)
        start_cycle_btn = QPushButton(self.tr("Start Cycle"))
        start_cycle_btn.clicked.connect(self.start_cycle)
        self.control_layout.addWidget(start_cycle_btn)
        main_layout.addLayout(self.control_layout)

        self.workout_table = QTableWidget()
        self.workout_table.setColumnCount(4)
        self.workout_table.setHorizontalHeaderLabels([
            self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
        ])
        main_layout.addWidget(self.workout_table)

        self.setStyleSheet("""
            QMainWindow {background-color: #f0f0f0;}
            QPushButton {background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px;}
            QPushButton:hover {background-color: #45a049;}
            QComboBox {border: 1px solid #ccc; border-radius: 5px; padding: 5px;}
            QTableWidget {border: 1px solid #ccc; background-color: white;}
        """)

    def change_language(self):
        language = self.language_combo.currentText()
        self.current_language = "ru" if language == "Русский" else "en"
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Fitness Tracker FST-8"))
        self.workout_table.setHorizontalHeaderLabels([
            self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
        ])
        # Обновляем текст виджетов в control_layout
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
        # Обновляем cycle_combo
        current_index = self.cycle_combo.currentIndex()
        self.cycle_combo.clear()
        self.cycle_combo.addItems([self.tr("8 weeks"), self.tr("10 weeks"), self.tr("12 weeks")])
        self.cycle_combo.setCurrentIndex(current_index if current_index >= 0 else 0)
        # Обновляем таблицу тренировок
        for row in range(self.workout_table.rowCount()):
            exercise_item = self.workout_table.item(row, 0)
            if exercise_item:
                current_exercise = exercise_item.text()
                for key, value in self.translations["en"].items():
                    if current_exercise == value or current_exercise == self.translations["ru"].get(key):
                        exercise_item.setText(self.tr(key))
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
        self.db.start_cycle(user_id, cycle_weeks, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        self.load_user_data()

    def load_user_data(self):
        user_id = self.user_combo.currentData()
        if not user_id:
            return
        cycle = self.db.get_user_cycle(user_id)
        if cycle:
            start_date = datetime.strptime(cycle[2], "%Y-%m-%d")
            end_date = datetime.strptime(cycle[3], "%Y-%m-%d")
            total_days = (end_date - start_date).days
            days_passed = (datetime.now() - start_date).days
            progress = min(100, (days_passed / total_days) * 100)
            self.progress_bar.setValue(int(progress))
            self.load_workouts(user_id, cycle[1])
        else:
            self.progress_bar.setValue(0)
            self.workout_table.setRowCount(0)

    def load_workouts(self, user_id, cycle_weeks):
        current_week = min(
            (datetime.now() - datetime.strptime(self.db.get_user_cycle(user_id)[2], "%Y-%m-%d")).days // 7 + 1,
            cycle_weeks)
        plan = WorkoutPlan(cycle_weeks, current_week)
        workouts = plan.get_workouts()
        self.workout_table.setRowCount(len(workouts))
        for i, workout in enumerate(workouts):
            self.workout_table.setItem(i, 0, QTableWidgetItem(self.tr(workout["exercise"])))
            self.workout_table.setItem(i, 1, QTableWidgetItem(str(workout["sets"])))
            self.workout_table.setItem(i, 2, QTableWidgetItem(str(workout["reps"])))
            weight = self.db.get_user_weight(user_id, workout["exercise"]) or workout["initial_weight"]
            self.workout_table.setItem(i, 3, QTableWidgetItem(str(weight)))