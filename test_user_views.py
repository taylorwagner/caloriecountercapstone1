"""User view tests."""

from unittest import TestCase
from models import db, connect_db, User
from app import app, CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///calcount_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser1", password="testuserpassword", email="testuser1@email.com", goal_cal=1000, city="Houston", state="TX")
        self.testuser_id = 909090
        self.testuser.id = self.testuser_id

        self.user1 = User.signup(username="user1", password="user1user1", email="user1@gmail.com", goal_cal=1110, city="New Orleans", state="LA")
        self.user1_id = 90909
        self.user1.id = self.user1_id
        self.user2 = User.signup(username="user2", password="user2pwpw", email="user2@yahoo.com", goal_cal=9999, city="Miami", state="FL")
        self.user2_id = 909099
        self.user2.id = self.user2_id
        self.user3 = User.signup("user3", "user33user3", "user3@user.com", 1234, "Lincoln", "NE")

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_show_profile(self):
        """Test feature that displays a user's profile page."""
        with self.client as c:
            res = c.get(f'/profile/{self.testuser_id}')

            self.assertEqual(res.status_code, 200)

            self.assertIn("testuser1", str(res.data))