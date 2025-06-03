from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import sys

try:
    import psycopg2
except ImportError:
    psycopg2 = None

# Determine Database URL
DEFAULT_SQLITE_URL = 'sqlite:///./health_app.db' # Use a distinct name for the app's default DB

if 'pytest' in sys.modules or 'unittest' in sys.modules or 'test' in sys.argv[0]:
    # Force SQLite for tests
    DATABASE_URL = 'sqlite:///./test.db'
    print("Running in test mode, using SQLite for test.db")
else:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL:
        print(f"Using DATABASE_URL from environment: {DATABASE_URL}")
        # If psycopg2 is None and DATABASE_URL starts with postgresql, it will fail at create_engine
        # This is acceptable as the user explicitly set a PostgreSQL URL.
    else:
        # Default to SQLite if DATABASE_URL is not set
        DATABASE_URL = DEFAULT_SQLITE_URL
        print(f"DATABASE_URL not set, defaulting to SQLite: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

from health_tracker.models import Base # Imports User, FoodEntry, etc. via __init__.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print(f"Initializing database at {DATABASE_URL}...")
    init_db()
    print("Database initialized successfully. Tables created (if they didn't exist).")
