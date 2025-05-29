import os
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

import unittest
from health_tracker.db import engine, get_db, init_db
from health_tracker.models.base import Base
from sqlalchemy.orm import Session
from sqlalchemy import inspect

class TestDatabaseSetup(unittest.TestCase):
    def setUp(self):
        # Create all tables in the test database
        init_db()

    def tearDown(self):
        # Drop all tables after tests
        Base.metadata.drop_all(bind=engine)

    def test_database_connection(self):
        # Test if we can get a session and query the database
        db_generator = get_db()
        db = next(db_generator)
        self.assertIsInstance(db, Session)
        db.close()

    def test_tables_exist(self):
        # Check if tables are created in the database
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        self.assertIn('users', tables)  # Assuming 'users' table exists
        self.assertIn('foodentries', tables)  # Assuming 'foodentries' table exists

if __name__ == '__main__':
    unittest.main()
