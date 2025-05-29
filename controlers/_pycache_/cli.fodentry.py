import click
from health_tracker.db import SessionLocal
from health_tracker.db_operations import create_foodentry, update_foodentry, delete_foodentry
from health_tracker.models import FoodEntry

@click.group()
def foodentry():
    
    pass

@foodentry.command()
@click.option('--user_id', required=True, type=int, help='User ID')
@click.option('--name', required=True, help='Food name')
@click.option('--calories', required=True, type=float, help='Calories')
@click.option('--protein', type=float, help='Protein')
@click.option('--fat', type=float, help='Fat')
@click.option('--carbs', type=float, help='Carbohydrates')
def create(user_id, name, calories, protein, fat, carbs):
    """Create a new food entry."""
    session = SessionLocal()
    foodentry = create_foodentry(session, user_id=user_id, name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    click.echo(f"FoodEntry created: {foodentry}")
    session.close()

@foodentry.command()
def list():
    """List all food entries."""
    session = SessionLocal()
    foodentries = session.query(FoodEntry).all()
    if not foodentries:
        click.echo("No food entries found.")
    else:
        for fe in foodentries:
            click.echo(f"ID: {fe.id}, User ID: {fe.user_id}, Name: {fe.name}, Calories: {fe.calories}")
    session.close()

@foodentry.command()
@click.option('--id', 'foodentry_id', required=True, type=int, help='FoodEntry ID')
@click.option('--name', help='New food name')
@click.option('--calories', type=float, help='New calories')
@click.option('--protein', type=float, help='New protein')
@click.option('--fat', type=float, help='New fat')
@click.option('--carbs', type=float, help='New carbohydrates')
def update(foodentry_id, name, calories, protein, fat, carbs):
    """Update a food entry."""
    session = SessionLocal()
    updated = update_foodentry(session, foodentry_id, name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    if updated:
        click.echo(f"FoodEntry updated: {updated}")
    else:
        click.echo("FoodEntry not found.")
    session.close()

@foodentry.command()
@click.option('--id', 'foodentry_id', required=True, type=int, help='FoodEntry ID')
def delete(foodentry_id):
    """Delete a food entry."""
    session = SessionLocal()
    success = delete_foodentry(session, foodentry_id)
    if success:
        click.echo("FoodEntry deleted.")
    else:
        click.echo("FoodEntry not found.")
    session.close()
