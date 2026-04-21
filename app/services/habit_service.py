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

def get_habit_stats(db, habit_id: int):
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id
    ).order_by(HabitLog.completed_at).all()

    if not logs:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "completion_rate": 0,
            "total_completed_days": 0
        }

    from datetime import date, timedelta

    log_dates = sorted([log.completed_at for log in logs])
    log_set = set(log_dates)

    # 🔥 CURRENT STREAK
    current_streak = 0
    today = date.today()

    while today in log_set:
        current_streak += 1
        today -= timedelta(days=1)

    # 🏆 LONGEST STREAK
    longest_streak = 0
    streak = 0

    prev_date = None

    for d in log_dates:
        if prev_date and (d - prev_date).days == 1:
            streak += 1
        else:
            streak = 1

        longest_streak = max(longest_streak, streak)
        prev_date = d

    # 📊 COMPLETION RATE
    first_day = log_dates[0]
    total_days = (date.today() - first_day).days + 1

    completion_rate = int((len(log_dates) / total_days) * 100)

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "completion_rate": completion_rate,
        "total_completed_days": len(log_dates)
    }

def get_habit_logs(db, habit_id: int):
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id
    ).order_by(HabitLog.completed_at).all()

    return [log.completed_at for log in logs]

def get_user_stats(db, user_id: int):
    from app.models.habit import Habit
    from app.models.habit_log import HabitLog

    habits = db.query(Habit).filter(Habit.user_id == user_id).all()

    if not habits:
        return {
            "total_habits": 0,
            "total_completed_days": 0,
            "best_streak": 0
        }

    habit_ids = [h.id for h in habits]

    logs = db.query(HabitLog).filter(
        HabitLog.habit_id.in_(habit_ids)
    ).all()

    total_completed_days = len(logs)

    # 🔥 calcular mejor streak global
    from datetime import timedelta

    best_streak = 0

    for habit in habits:
        dates = db.query(HabitLog.completed_at).filter(
            HabitLog.habit_id == habit.id
        ).order_by(HabitLog.completed_at).all()

        dates = [d[0] for d in dates]

        streak = 0
        prev = None

        for d in dates:
            if prev and (d - prev).days == 1:
                streak += 1
            else:
                streak = 1

            best_streak = max(best_streak, streak)
            prev = d

    return {
        "total_habits": len(habits),
        "total_completed_days": total_completed_days,
        "best_streak": best_streak
    }