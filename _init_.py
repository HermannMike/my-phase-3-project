"""
Health Simplified CLI Application Package Initialization

This file initializes the Health Simplified package, making it easier to import
and use the main components of the application. It defines what is available
when someone uses `from health_simplified import *` and imports the main
components for direct access.
"""

__all__ = ['models', 'cli']

# Import the main components of the package for easy access
from .models import Base, User, FoodEntry, Goal, MealPlan
from .cli import cli
