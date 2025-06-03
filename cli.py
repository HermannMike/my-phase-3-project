# CLI entry point using click for the Health Simplified CLI Application

import click
from datetime import datetime
from health_tracker.db import init_db, SessionLocal
from health_tracker.models import User, FoodEntry, Goal, MealPlan # Added Goal and MealPlan

@click.group()
def cli():
    """Health Simplified CLI Application"""
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

# User management commands
@cli.group()
def user():
    """User management commands."""
    pass

@user.command()
@click.option('--name', required=True, help='Name of the user')
def create(name):
    """Create a new user."""
    session = SessionLocal()
    if session.query(User).filter_by(name=name).first():
        click.echo(f"User '{name}' already exists.")
        session.close()
        return
    user = User(name=name)
    session.add(user)
    session.commit()
    click.echo(f"User '{name}' created.")
    session.close()

@user.command()
def list():
    """List all users."""
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.name}")
    session.close()
@user.command()
@click.option('--name', required=True, help='Name of the user to delete.')
@click.confirmation_option(prompt='Are you sure you want to delete this user and all their associated data?')
def delete(name):
    """Delete a user and all their associated data (food entries, goals, meal plans)."""
    session = SessionLocal()
    user_to_delete = session.query(User).filter_by(name=name).first()

    if not user_to_delete:
        click.echo(f"Error: User '{name}' not found.")
        session.close()
        return

    try:
        # Delete associated food entries
        session.query(FoodEntry).filter_by(user_id=user_to_delete.id).delete()
        # Delete associated goals
        session.query(Goal).filter_by(user_id=user_to_delete.id).delete()
        # Delete associated meal plans
        session.query(MealPlan).filter_by(user_id=user_to_delete.id).delete()
        
        # Delete the user
        session.delete(user_to_delete)
        
        session.commit()
        click.echo(f"User '{name}' and all associated data have been deleted.")
    except Exception as e:
        session.rollback()
        click.echo(f"An error occurred while deleting user '{name}': {e}")
    finally:
        session.close()

# Food entry commands
@cli.group()
def entry():
    """Food entry management commands."""
    pass

@entry.command()
@click.option('--user', 'user_name', required=True, help='Name of the user logging the entry.')
@click.option('--food', 'food_name', required=True, help='Name of the food item.')
@click.option('--calories', required=True, type=int, help='Number of calories.')
@click.option('--date', 'date_str', required=True, help='Date of consumption (YYYY-MM-DD).')
def add(user_name, food_name, calories, date_str):
    """Add a new food entry for a user."""
    session = SessionLocal()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        click.echo(f"Error: User '{user_name}' not found.")
        session.close()
        return

    try:
        entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        click.echo("Error: Date format must be YYYY-MM-DD.")
        session.close()
        return

    food_entry = FoodEntry(
        user_id=user.id,
        food_name=food_name,
        calories=calories,
        date=entry_date
    )
    session.add(food_entry)
    session.commit()
    click.echo(f"Food entry '{food_name}' ({calories} kcal) added for user '{user_name}' on {date_str}.")
    session.close()
@entry.command('list') # Explicitly naming command to avoid conflict with built-in list
@click.option('--user', 'user_name', help='Name of the user to filter entries for.')
@click.option('--date', 'date_str', help='Date to filter entries for (YYYY-MM-DD).')
def list_entries(user_name, date_str):
    """List food entries, optionally filtered by user and/or date."""
    session = SessionLocal()
    query = session.query(FoodEntry)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            click.echo(f"Error: User '{user_name}' not found.")
            session.close()
            return
        query = query.filter(FoodEntry.user_id == user.id)

    if date_str:
        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(FoodEntry.date == filter_date)
        except ValueError:
            click.echo("Error: Date format for filtering must be YYYY-MM-DD.")
            session.close()
            return

    entries = query.all()

    if not entries:
        click.echo("No food entries found matching your criteria.")
    else:
        click.echo("Food Entries:")
        for entry in entries:
            user = session.query(User).filter_by(id=entry.user_id).first() # Get user name for display
            click.echo(
                f"  ID: {entry.id}, User: {user.name if user else 'N/A'}, Food: {entry.food_name}, "
                f"Calories: {entry.calories}, Date: {entry.date.strftime('%Y-%m-%d')}"
            )
    session.close()


if __name__ == '__main__':
    cli()
