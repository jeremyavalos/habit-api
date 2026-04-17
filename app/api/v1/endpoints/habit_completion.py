from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.utils.security import get_current_user
from app.services.habit_completion_service import (
    complete_habit,
    get_habit_streak
)

router = APIRouter()


# 🔹 Marcar hábito como completado
@router.post("/complete")
def complete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return complete_habit(
        db=db,
        user_id=current_user.id,
        habit_id=habit_id,
        completion_date=date.today()
    )


# 🔥 Obtener streak
@router.get("/{habit_id}/streak")
def get_streak(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_habit_streak(db, habit_id, current_user.id)