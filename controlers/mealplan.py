from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class MealPlan(Base):
    __tablename__ = 'mealplans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)  # e.g., breakfast, lunch, dinner, snack

    user = relationship('User', back_populates='mealplans')

    def __repr__(self):
        return f"<MealPlan(id={self.id}, date={self.date}, meal_type='{self.meal_type}')>"
