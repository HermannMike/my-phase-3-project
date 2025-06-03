from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    food_entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False) # Assuming one active goal per user
    meal_plans = relationship("MealPlan", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="food_entries")

    def __repr__(self):
        return f"<FoodEntry(id={self.id}, food_name='{self.food_name}', calories={self.calories}, date='{self.date}')>"

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False) # One goal per user
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)

    user = relationship("User", back_populates="goals")

    def __repr__(self):
        return f"<Goal(id={self.id}, user_id={self.user_id}, daily_calories={self.daily_calories}, weekly_calories={self.weekly_calories})>"

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False) # e.g., 202523 for 23rd week of 2025
    details = Column(String, nullable=True) # Simple text details for now

    user = relationship("User", back_populates="meal_plans")

    def __repr__(self):
        return f"<MealPlan(id={self.id}, user_id={self.user_id}, week_number={self.week_number})>"