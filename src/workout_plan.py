from datetime import datetime, timedelta
import logging
import os

# Setup logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fittracker.log"),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WorkoutPlan:
    # Define compound exercises for larger increments
    COMPOUND_EXERCISES = [
        "Bench Press", "Squat", "Leg Press", "Bent-over Row", "Overhead Barbell Press", "Pull-up"
    ]

    def __init__(self, cycle_weeks, current_week, training_days=5):
        self.cycle_weeks = cycle_weeks
        self.current_week = min(current_week, cycle_weeks)
        self.training_days = training_days  # 3 or 5 days
        self.training_split = self.get_training_split()
        logging.info(f"Initialized WorkoutPlan: {cycle_weeks} weeks, week {current_week}, {training_days}-day split")

    def get_training_split(self):
        if self.training_days == 5:
            return [
                # Day 1: Chest
                [
                    {"exercise": "Bench Press", "sets": 4, "reps": "8-12", "initial_weight": 60, "rest": 120},
                    {"exercise": "Incline Dumbbell Press", "sets": 3, "reps": "8-12", "initial_weight": 20, "rest": 120},
                    {"exercise": "Hammer Strength Chest Press", "sets": 3, "reps": "10-12", "initial_weight": 40, "rest": 120},
                    {"exercise": "Cable Crossover", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ],
                # Day 2: Back
                [
                    {"exercise": "Bent-over Row", "sets": 4, "reps": "8-12", "initial_weight": 60, "rest": 120},
                    {"exercise": "Pull-up", "sets": 3, "reps": "8-12", "initial_weight": 0, "rest": 120},
                    {"exercise": "Seated Cable Row", "sets": 3, "reps": "10-12", "initial_weight": 40, "rest": 120},
                    {"exercise": "Cable Pullover", "sets": 7, "reps": "10-12", "initial_weight": 15, "rest": 30, "fst7": True}
                ],
                # Day 3: Legs
                [
                    {"exercise": "Squat", "sets": 4, "reps": "8-12", "initial_weight": 80, "rest": 120},
                    {"exercise": "Leg Press", "sets": 3, "reps": "8-12", "initial_weight": 100, "rest": 120},
                    {"exercise": "Lying Leg Curl", "sets": 3, "reps": "10-12", "initial_weight": 30, "rest": 120},
                    {"exercise": "Leg Extension", "sets": 7, "reps": "10-12", "initial_weight": 20, "rest": 30, "fst7": True}
                ],
                # Day 4: Shoulders
                [
                    {"exercise": "Overhead Barbell Press", "sets": 4, "reps": "8-12", "initial_weight": 40, "rest": 120},
                    {"exercise": "Dumbbell Lateral Raise", "sets": 3, "reps": "8-12", "initial_weight": 10, "rest": 120},
                    {"exercise": "Machine Shoulder Press", "sets": 3, "reps": "10-12", "initial_weight": 30, "rest": 120},
                    {"exercise": "Machine Lateral Raise", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ],
                # Day 5: Arms (Biceps + Triceps)
                [
                    {"exercise": "EZ-Bar Curl", "sets": 3, "reps": "8-12", "initial_weight": 20, "rest": 120},
                    {"exercise": "Cable Pushdown", "sets": 3, "reps": "8-12", "initial_weight": 15, "rest": 120},
                    {"exercise": "Hammer Curl", "sets": 3, "reps": "10-12", "initial_weight": 10, "rest": 120},
                    {"exercise": "Tricep Dip", "sets": 3, "reps": "10-12", "initial_weight": 0, "rest": 120},
                    {"exercise": "Machine Curl", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True},
                    {"exercise": "Machine Tricep Extension", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ]
            ]
        else:  # 3-day split
            return [
                # Day 1: Chest + Biceps
                [
                    {"exercise": "Bench Press", "sets": 4, "reps": "8-12", "initial_weight": 60, "rest": 120},
                    {"exercise": "Incline Dumbbell Press", "sets": 3, "reps": "8-12", "initial_weight": 20, "rest": 120},
                    {"exercise": "Cable Crossover", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True},
                    {"exercise": "EZ-Bar Curl", "sets": 3, "reps": "8-12", "initial_weight": 20, "rest": 120},
                    {"exercise": "Hammer Curl", "sets": 3, "reps": "10-12", "initial_weight": 10, "rest": 120},
                    {"exercise": "Machine Curl", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ],
                # Day 2: Back + Triceps
                [
                    {"exercise": "Bent-over Row", "sets": 4, "reps": "8-12", "initial_weight": 60, "rest": 120},
                    {"exercise": "Pull-up", "sets": 3, "reps": "8-12", "initial_weight": 0, "rest": 120},
                    {"exercise": "Cable Pullover", "sets": 7, "reps": "10-12", "initial_weight": 15, "rest": 30, "fst7": True},
                    {"exercise": "Cable Pushdown", "sets": 3, "reps": "8-12", "initial_weight": 15, "rest": 120},
                    {"exercise": "Tricep Dip", "sets": 3, "reps": "10-12", "initial_weight": 0, "rest": 120},
                    {"exercise": "Machine Tricep Extension", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ],
                # Day 3: Legs + Shoulders
                [
                    {"exercise": "Squat", "sets": 4, "reps": "8-12", "initial_weight": 80, "rest": 120},
                    {"exercise": "Leg Press", "sets": 3, "reps": "8-12", "initial_weight": 100, "rest": 120},
                    {"exercise": "Leg Extension", "sets": 7, "reps": "10-12", "initial_weight": 20, "rest": 30, "fst7": True},
                    {"exercise": "Overhead Barbell Press", "sets": 4, "reps": "8-12", "initial_weight": 40, "rest": 120},
                    {"exercise": "Dumbbell Lateral Raise", "sets": 3, "reps": "8-12", "initial_weight": 10, "rest": 120},
                    {"exercise": "Machine Lateral Raise", "sets": 7, "reps": "10-12", "initial_weight": 10, "rest": 30, "fst7": True}
                ]
            ]

    def get_weight_increment(self, exercise, current_weight, week):
        """Calculate the weight increment based on exercise type and cycle week."""
        is_compound = exercise in self.COMPOUND_EXERCISES
        if is_compound:
            # Compound exercises: larger increments early, smaller later
            if self.cycle_weeks == 8:
                if week <= 2:
                    return 10  # First 2 weeks: +10 kg
                elif week <= 6:
                    return 5   # Weeks 3-6: +5 kg
                else:
                    return 2.5 # Last 2 weeks: +2.5 kg
            elif self.cycle_weeks == 10:
                if week <= 3:
                    return 8
                elif week <= 7:
                    return 4
                else:
                    return 2
            else:  # 12 weeks
                if week <= 4:
                    return 7
                elif week <= 8:
                    return 3.5
                else:
                    return 1.75
        else:
            # Isolation exercises: smaller increments
            if self.cycle_weeks == 8:
                return 1.25  # Consistent small increment
            elif self.cycle_weeks == 10:
                return 1
            else:  # 12 weeks
                return 0.75

    def get_workouts(self, user_id, db):
        """Get workouts with updated weights based on progression."""
        current_day = datetime.now().weekday()
        if self.training_days == 3:
            if current_day in [0, 2, 4]:  # Mon, Wed, Fri
                day_index = [0, 1, 2][[0, 2, 4].index(current_day)]
            else:
                day_index = 0  # Default to first workout on rest days
        else:  # 5-day split
            day_index = 0 if current_day >= 5 else current_day  # Default to Day 1 (Chest) on rest days

        workouts = self.training_split[day_index]
        logging.info(f"Selected workouts for day_index {day_index}: {workouts}")
        for workout in workouts:
            # Get last weight from DB or use initial
            last_weight = db.get_user_weight(user_id, workout["exercise"]) or workout["initial_weight"]
            # Calculate next weight
            increment = self.get_weight_increment(workout["exercise"], last_weight, self.current_week)
            workout["suggested_weight"] = last_weight + increment
        return workouts

    def complete_workout(self, db, user_id):
        """Save the current workout to the database."""
        workouts = self.get_workouts(user_id, db)
        date = datetime.now().strftime("%Y-%m-%d")
        for workout in workouts:
            db.save_workout(
                user_id=user_id,
                exercise=workout["exercise"],
                sets=workout["sets"],
                reps=workout["reps"],
                weight=workout["suggested_weight"],
                date=date
            )
        logging.info(f"Completed workout for user_id {user_id} on {date}")

    def start_cycle(self, db, user_id):
        """Start a new training cycle."""
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(weeks=self.cycle_weeks)).strftime("%Y-%m-%d")
        db.start_cycle(user_id, self.cycle_weeks, start_date, end_date)
        logging.info(f"Started cycle for user_id {user_id}: {self.cycle_weeks} weeks")