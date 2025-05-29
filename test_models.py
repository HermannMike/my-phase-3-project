import unittest
from health_tracker.db import engine, SessionLocal, init_db
from health_tracker.models.base import Base
from health_tracker.models.user import User
from health_tracker.models.foodentry import FoodEntry

class TestModelsCRUD(unittest.TestCase):
    def setUp(self):
        init_db()
        self.session = SessionLocal()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(bind=engine)

    def test_user_crud(self):
        # Create
        user = User(username='testuser', email='test@example.com')
        self.session.add(user)
        self.session.commit()
        self.assertIsNotNone(user.id)

        # Read
        fetched_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertEqual(fetched_user.email, 'test@example.com')

        # Update
        fetched_user.email = 'newemail@example.com'
        self.session.commit()
        updated_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertEqual(updated_user.email, 'newemail@example.com')

        # Delete
        self.session.delete(updated_user)
        self.session.commit()
        deleted_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertIsNone(deleted_user)

    def test_foodentry_crud(self):
        # Create user first
        user = User(username='fooduser', email='food@example.com')
        self.session.add(user)
        self.session.commit()

        # Create FoodEntry
        foodentry = FoodEntry(user_id=user.id, name='Apple', calories=95.0, protein=0.5, fat=0.3, carbs=25.0)
        self.session.add(foodentry)
        self.session.commit()
        self.assertIsNotNone(foodentry.id)

        # Read
        fetched_fe = self.session.query(FoodEntry).filter_by(name='Apple').first()
        self.assertEqual(fetched_fe.calories, 95.0)

        # Update
        fetched_fe.calories = 100.0
        self.session.commit()
        updated_fe = self.session.query(FoodEntry).filter_by(name='Apple').first()
        self.assertEqual(updated_fe.calories, 100.0)

        # Delete
        self.session.delete(updated_fe)
        self.session.commit()
        deleted_fe = self.session.query(FoodEntry).filter_by(name='Apple').first()
        self.assertIsNone(deleted_fe)

if __name__ == '__main__':
    unittest.main()
