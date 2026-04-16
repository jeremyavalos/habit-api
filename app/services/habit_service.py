from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.schemas.habit import HabitCreate
from fastapi import HTTPException
from app.models.habit import Habit


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