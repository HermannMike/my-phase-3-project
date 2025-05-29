import unittest
from click.testing import CliRunner
from health_tracker.models.controlers.cli_foodentry import foodentry
from health_tracker.db import init_db, SessionLocal
from health_tracker.models.base import Base
from health_tracker.models.user import User

class TestCLI_FoodEntry(unittest.TestCase):
    def setUp(self):
        init_db()
        self.runner = CliRunner()
        self.session = SessionLocal()
        # Create a user for foodentry commands
        self.user = User(username='cliuser', email='cliuser@example.com')
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(bind=self.session.bind)

    def test_create_list_update_delete_foodentry(self):
        # Create foodentry
        result = self.runner.invoke(foodentry, ['create', '--user_id', str(self.user.id), '--name', 'Banana', '--calories', '105'])
        self.assertIn('FoodEntry created', result.output)

        # List foodentries
        result = self.runner.invoke(foodentry, ['list'])
        self.assertIn('Banana', result.output)

        # Get foodentry id from list output (simple parse)
        lines = result.output.splitlines()
        foodentry_id = None
        for line in lines:
            if 'Banana' in line:
                parts = line.split(',')
                for part in parts:
                    if part.strip().startswith('ID:'):
                        foodentry_id = part.strip().split(' ')[1]
                        break
        self.assertIsNotNone(foodentry_id)

        # Update foodentry
        result = self.runner.invoke(foodentry, ['update', '--id', foodentry_id, '--calories', '110'])
        self.assertIn('FoodEntry updated', result.output)

        # Delete foodentry
        result = self.runner.invoke(foodentry, ['delete', '--id', foodentry_id])
        self.assertIn('FoodEntry deleted', result.output)

        # List again to confirm deletion
        result = self.runner.invoke(foodentry, ['list'])
        self.assertIn('No food entries found', result.output)

if __name__ == '__main__':
    unittest.main()
