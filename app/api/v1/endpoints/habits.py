from app.services.habit_service import get_habit_logs
from app.services.habit_service import get_habit_stats
from app.services.habit_service import get_streak
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.habit import HabitCreate
from app.utils.security import get_current_user
from app.services.habit_service import (
    create_habit,
    get_user_habits,
    complete_habit,
    delete_habit
)

router = APIRouter()


@router.post("/")
def create_habit_endpoint(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_habit(db, habit, current_user.id)


@router.get("/")
def get_habits(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_habits(db, current_user.id)


@router.patch("/{habit_id}")
def complete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return complete_habit(db, habit_id, current_user.id)


@router.delete("/{habit_id}")
def delete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return delete_habit(db, habit_id, current_user.id)

@router.get("/{habit_id}/streak")
def get_habit_streak(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return {
        "streak": get_streak(db, habit_id)
    }

@router.get("/{habit_id}/stats")
def habit_stats(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_habit_stats(db, habit_id)


@router.get("/{habit_id}/logs")
def habit_logs(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_habit_logs(db, habit_id)