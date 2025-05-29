import unittest
from click.testing import CliRunner
from health_tracker.models.controlers.cli_mealplan import mealplan
from health_tracker.db import init_db, SessionLocal
from health_tracker.models.base import Base
from health_tracker.models.user import User

class TestCLI_MealPlan(unittest.TestCase):
    def setUp(self):
        init_db()
        self.runner = CliRunner()
        self.session = SessionLocal()
        # Create a user for mealplan commands
        self.user = User(username='cliuser2', email='cliuser2@example.com')
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(bind=self.session.bind)

    def test_create_list_update_delete_mealplan(self):
        # Create mealplan
        result = self.runner.invoke(mealplan, ['create', '--user_id', str(self.user.id), '--date', '2023-01-01', '--meal_type', 'breakfast'])
        self.assertIn('MealPlan created', result.output)

        # List mealplans
        result = self.runner.invoke(mealplan, ['list'])
        self.assertIn('breakfast', result.output)

        # Get mealplan id from list output (simple parse)
        lines = result.output.splitlines()
        mealplan_id = None
        for line in lines:
            if 'breakfast' in line:
                parts = line.split(',')
                for part in parts:
                    if part.strip().startswith('ID:'):
                        mealplan_id = part.strip().split(' ')[1]
                        break
        self.assertIsNotNone(mealplan_id)

        # Update mealplan
        result = self.runner.invoke(mealplan, ['update', '--id', mealplan_id, '--meal_type', 'lunch'])
        self.assertIn('MealPlan updated', result.output)

        # Delete mealplan
        result = self.runner.invoke(mealplan, ['delete', '--id', mealplan_id])
        self.assertIn('MealPlan deleted', result.output)

        # List again to confirm deletion
        result = self.runner.invoke(mealplan, ['list'])
        self.assertIn('No mealplans found', result.output)

if __name__ == '__main__':
    unittest.main()
