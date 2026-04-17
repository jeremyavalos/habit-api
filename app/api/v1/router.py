from fastapi import APIRouter

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import habits
from app.api.v1.endpoints import habit_completion


api_router = APIRouter()

# 🔐 Auth
api_router.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Auth"]
)

# 📌 Habits CRUD
api_router.include_router(
    habits.router,
    prefix="/api/v1/habits",
    tags=["Habits"]
)

# 🔥 Completions (SEPARADO)
api_router.include_router(
    habit_completion.router,
    prefix="/api/v1/completions",
    tags=["Completions"]
)