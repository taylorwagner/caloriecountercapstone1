"""Group view tests."""

from unittest import TestCase
from models import db, connect_db, User, Group, UserGroup
from app import app, CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///calcount_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.create_all()


class GroupViewTestCase(TestCase):
    """Test views for group."""
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="grouptestuser1", password="testgroupviews", email="grouptestuser1@email.com", goal_cal=5000, city="San Antonio", state="TX")
        self.testuser_id = 999991
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
