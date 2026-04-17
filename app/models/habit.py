from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔥 RELACIÓN CON COMPLETIONS (CLAVE PARA STREAKS)
    completions = relationship(
        "HabitCompletion",
        back_populates="habit",
        cascade="all, delete"
    )