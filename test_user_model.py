"""User and Follows model tests."""

from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Follows
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///calcount_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test model for user."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        testuser1 = User.signup("testuser1", "password", "test@testing.com", 1500, "Lincoln", "NE")
        testuser1id = 999999
        testuser1.id = testuser1id

        testuser2 = User.signup("testu", "passwordtest", "test@email.com", 1000, "Houston", "TX")
        testuser2id = 999998
        testuser2.id = testuser2id

        db.session.commit()

        testuser1 = User.query.get(testuser1id)
        testuser2 = User.query.get(testuser2id)

        self.testuser1 = testuser1
        self.testuser1id = testuser1id

        self.testuser2 = testuser2
        self.testuser2id = testuser2id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        fakeu = User(email="fake@fake.com", username="fakeu", password="shouldbehashed", city="city", state="FL", goal_cal=3000)

        db.session.add(fakeu)
        db.session.commit()

        # User should have no followers and following no one
        self.assertEqual(len(fakeu.followers), 0)
        self.assertEqual(len(fakeu.following), 0)