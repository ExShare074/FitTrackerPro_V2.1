from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QDialog, QCalendarWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
from src.workout_plan import WorkoutPlan

class FitnessTrackerApp(QMainWindow):
    translations = {
        "en": {
            "Fitness Tracker FST-8": "Fitness Tracker FST-7",
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
            "Machine Tricep Extension": "Machine Tricep Extension"
        },
        "ru": {
            "Fitness Tracker FST-8": "Фитнес-трекер FST-7",
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
            "Hammer Curl": "Молотковый сгиб",
            "Hammer Strength Chest Press": "Жим в тренажере Hammer Strength",
            "Cable Crossover": "Кабельные кроссоверы",
            "Seated Cable Row": "Тяга блока сидя",
            "Cable Pullover": "Пулловеры на блоке",
            "Lying Leg Curl": "Сгибания ног лежа",
            "Leg Extension": "Разгибания ног",
            "Machine Shoulder Press": "Жим в тренажере для плеч",
            "Machine Lateral Raise": "Боковые подъемы в тренажере",
            "Cable Pushdown": "Разгибания на трицепс с канатом",
            "Machine Curl": "Сгибания на бицепс в тренажере",
            "Machine Tricep Extension": "Разгибания на трицепс в тренажере"
        }
    }

    def __init__(self, db):
        super().__init__()
        self.db = db
        lang = self.db.conn.execute("SELECT value FROM settings WHERE key = 'language'").fetchone()
        self.current_language = lang[0] if lang else "en"
        self.control_layout = None
        self.setWindowTitle(self.tr("Fitness Tracker FST-7"))
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

        self.training_days_combo = QComboBox()
        self.training_days_combo.addItem(self.tr("5-day Split"), 5)
        self.training_days_combo.addItem(self.tr("3-day Split"), 3)
        self.training_days_combo.currentIndexChanged.connect(self.load_user_data)
        self.control_layout.addWidget(QLabel(self.tr("Training Split:")))
        self.control_layout.addWidget(self.training_days_combo)

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
        self.workout_table.itemChanged.connect(self.update_weight)
        main_layout.addWidget(self.workout_table)

        complete_workout_btn = QPushButton(self.tr("Complete Workout"))
        complete_workout_btn.clicked.connect(self.complete_workout)
        main_layout.addWidget(complete_workout_btn)

        history_btn = QPushButton(self.tr("View History"))
        history_btn.clicked.connect(self.view_history)
        main_layout.addWidget(history_btn)

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
        self.db.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                            ("language", self.current_language))
        self.db.conn.commit()
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Fitness Tracker FST-7"))
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
        self.db.start_cycle(user_id, cycle_weeks, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        self.load_user_data()

    def load_user_data(self):
        user_id = self.user_combo.currentData()
        if user_id:
            self.db.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                                ("last_user", str(user_id)))
            self.db.conn.commit()
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
        current_week = min((datetime.now() - datetime.strptime(self.db.get_user_cycle(user_id)[2], "%Y-%m-%d")).days // 7 + 1, cycle_weeks)
        plan = WorkoutPlan(cycle_weeks, current_week, self.training_days_combo.currentData())
        workouts = plan.get_workouts(user_id, self.db)
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
            exercise = self.workout_table.item(row, 0).text().replace(" (FST-7)", "")
            sets = int(self.workout_table.item(row, 1).text())
            reps = self.workout_table.item(row, 2).text().split('-')[-1]
            try:
                weight = float(self.workout_table.item(row, 3).text())
            except ValueError:
                QMessageBox.warning(self, self.tr("Error"), "Invalid weight in row {}".format(row + 1))
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
        self.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.load_workouts_for_date)
        layout.addWidget(self.calendar)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([self.tr("Muscle Group"), self.tr("Date")])
        layout.addWidget(self.tree)

        # Highlight completed workout dates
        workouts = self.db.conn.execute("SELECT DISTINCT date FROM workouts WHERE user_id = ?", (self.user_id,)).fetchall()
        for workout in workouts:
            date = datetime.strptime(workout[0], "%Y-%m-%d").date()
            format = self.calendar.dateTextFormat(date)
            format.setBackground(Qt.green)
            self.calendar.setDateTextFormat(date, format)

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

        for group, group_workouts in workouts_by_group.items():
            group_item = QTreeWidgetItem(self.tree, [self.tr(group), date_str])
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels([
                self.tr("Exercise"), self.tr("Sets"), self.tr("Reps"), self.tr("Weight (kg)")
            ])
            table.setRowCount(len(group_workouts))
            for i, (exercise, sets, reps, weight) in enumerate(group_workouts):
                table.setItem(i, 0, QTableWidgetItem(self.tr(exercise)))
                table.setItem(i, 1, QTableWidgetItem(str(sets)))
                table.setItem(i, 2, QTableWidgetItem(str(reps)))
                table.setItem(i, 3, QTableWidgetItem(str(weight)))
            table.resizeColumnsToContents()
            self.tree.setItemWidget(group_item, 0, table)