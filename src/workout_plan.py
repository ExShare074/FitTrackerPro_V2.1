class WorkoutPlan:
    def __init__(self, cycle_weeks, current_week):
        self.cycle_weeks = cycle_weeks
        self.current_week = current_week
        self.exercises = {
            "Chest": ["Bench Press", "Dumbbell Press", "Incline Bench Press"],
            "Back": ["Deadlift", "Bent-over Row", "Pull-up"],
            "Legs": ["Squat", "Leg Press", "Lunges"],
            "Shoulders": ["Overhead Press", "Dumbbell Raise", "Barbell Shrug"],
            "Arms": ["Bicep Curl", "Tricep Dip", "Hammer Curl"]
        }
        self.progression = {
            "Bench Press": {"initial_weight": 50, "step": 2.5, "frequency": 1},
            "Dumbbell Press": {"initial_weight": 20, "step": 2, "frequency": 1},
            "Incline Bench Press": {"initial_weight": 40, "step": 2.5, "frequency": 1},
            "Deadlift": {"initial_weight": 60, "step": 5, "frequency": 1},
            "Bent-over Row": {"initial_weight": 40, "step": 2.5, "frequency": 1},
            "Pull-up": {"initial_weight": 0, "step": 0, "frequency": 1},
            "Squat": {"initial_weight": 60, "step": 5, "frequency": 1},
            "Leg Press": {"initial_weight": 80, "step": 5, "frequency": 1},
            "Lunges": {"initial_weight": 20, "step": 2, "frequency": 1},
            "Overhead Press": {"initial_weight": 30, "step": 2.5, "frequency": 1},
            "Dumbbell Raise": {"initial_weight": 10, "step": 1, "frequency": 2},
            "Barbell Shrug": {"initial_weight": 40, "step": 2.5, "frequency": 1},
            "Bicep Curl": {"initial_weight": 10, "step": 1, "frequency": 2},
            "Tricep Dip": {"initial_weight": 0, "step": 0, "frequency": 1},
            "Hammer Curl": {"initial_weight": 10, "step": 1, "frequency": 2}
        }

    def get_workouts(self):
        workouts = []
        week_index = (self.current_week - 1) % 3  # Цикл смены упражнений каждую неделю
        for muscle_group, exercises in self.exercises.items():
            exercise = exercises[week_index]
            sets = 8 if exercise in ["Bicep Curl", "Tricep Dip", "Hammer Curl"] else 4  # FST-8 для изолирующих
            reps = "8-12" if exercise in ["Bicep Curl", "Tricep Dip", "Hammer Curl"] else "10-12"
            workouts.append({
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "initial_weight": self.progression[exercise]["initial_weight"]
            })
        return workouts