from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date

from app.database import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    completed_at = Column(Date, default=date.today)

    habit = relationship("Habit")