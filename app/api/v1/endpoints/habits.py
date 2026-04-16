from app.services.habit_service import (
    create_habit,
    get_user_habits,
    complete_habit,
    delete_habit
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.habit import HabitCreate
from app.core.security import get_current_user
from app.services.habit_service import create_habit, get_user_habits

router = APIRouter()


@router.post("/")
def create_habit_endpoint(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_habit(db, habit, int(user["sub"]))


@router.get("/")
def get_habits(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_user_habits(db, int(user["sub"]))

@router.patch("/{habit_id}")
def complete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return complete_habit(db, habit_id, int(user["sub"]))

@router.delete("/{habit_id}")
def delete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return delete_habit(db, habit_id, int(user["sub"]))
