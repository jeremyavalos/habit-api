from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion


# 🔹 Validar que el hábito pertenece al usuario
def get_user_habit(db: Session, habit_id: int, user_id: int):
    return db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == user_id
    ).first()


# 🔹 Marcar hábito como completado (IDEMPOTENTE)
def complete_habit(
    db: Session,
    user_id: int,
    habit_id: int,
    completion_date: date
):
    habit = get_user_habit(db, habit_id, user_id)

    if not habit:
        raise Exception("Habit not found or not owned by user")

    existing = db.query(HabitCompletion).filter(
        HabitCompletion.habit_id == habit_id,
        HabitCompletion.date == completion_date
    ).first()

    if existing:
        return existing

    completion = HabitCompletion(
        habit_id=habit_id,
        user_id=user_id,
        date=completion_date
    )

    db.add(completion)
    db.commit()
    db.refresh(completion)

    return completion


# 🔹 Obtener historial
def get_habit_history(db: Session, habit_id: int, user_id: int):
    return db.query(HabitCompletion).filter(
        HabitCompletion.habit_id == habit_id,
        HabitCompletion.user_id == user_id
    ).order_by(HabitCompletion.date.asc()).all()


# 🔥 CALCULAR STREAK ACTUAL
def calculate_current_streak(dates: list[date]) -> int:
    if not dates:
        return 0

    dates = sorted(dates, reverse=True)

    today = date.today()
    streak = 0

    for i, d in enumerate(dates):
        expected_day = today - timedelta(days=i)

        if d == expected_day:
            streak += 1
        else:
            break

    return streak


# 🔹 Obtener streak del hábito
def get_habit_streak(db: Session, habit_id: int, user_id: int):
    history = get_habit_history(db, habit_id, user_id)

    dates = [h.date for h in history]

    current_streak = calculate_current_streak(dates)

    return {
        "current_streak": current_streak,
        "total_days": len(dates)
    }