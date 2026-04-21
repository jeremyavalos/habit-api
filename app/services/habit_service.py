from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.schemas.habit import HabitCreate
from fastapi import HTTPException
from app.models.habit import Habit
from datetime import date
from app.models.habit_log import HabitLog
from datetime import date, timedelta
from app.models.habit_log import HabitLog


def get_streak(db, habit_id: int):
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id
    ).order_by(HabitLog.completed_at.desc()).all()

    if not logs:
        return 0

    streak = 0
    current_day = date.today()

    log_dates = {log.completed_at for log in logs}

    while current_day in log_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak

def complete_habit(db, habit_id: int, user_id: int):
    today = date.today()

    # 🔹 evitar duplicado
    existing = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.completed_at == today
    ).first()

    if existing:
        return {"message": "Ya completado hoy"}

    log = HabitLog(
        habit_id=habit_id,
        completed_at=today
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {"message": "Hábito completado"}

def complete_habit(db, habit_id: int, user_id: int):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit no encontrado")

    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    habit.completed = True

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(db, habit_id: int, user_id: int):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit no encontrado")

    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    db.delete(habit)
    db.commit()

    return {"message": "Habit eliminado"}

def create_habit(db: Session, habit: HabitCreate, user_id: int):
    new_habit = Habit(
        title=habit.title,
        user_id=user_id
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit


def get_user_habits(db: Session, user_id: int):
    return db.query(Habit).filter(Habit.user_id == user_id).all()