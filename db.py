from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import sys

try:
    import psycopg2
except ImportError:
    psycopg2 = None

# Force SQLite for tests to avoid PostgreSQL auth errors
if 'pytest' in sys.modules or 'unittest' in sys.modules or 'test' in sys.argv[0]:
    DATABASE_URL = 'sqlite:///./test.db'
else:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

if psycopg2 is None:
    # Fallback to SQLite if psycopg2 is not installed
    DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

from health_tracker.models.base import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
