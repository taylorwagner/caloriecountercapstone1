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

# SIGNUP TESTS

    def test_valid_signup(self):
        """Test that a new user will register when validly signing up."""
        fakeuser = User.signup("fakeuser", "password", "test@gmail.com", 1500, "Lincoln", "NE")
        fakeuserid = 9999
        fakeuser.id = fakeuserid
        db.session.commit()

        fakeuser = User.query.get(fakeuserid)
        self.assertIsNotNone(fakeuser)
        self.assertEqual(fakeuser.username, "fakeuser")
        self.assertEqual(fakeuser.email, "test@gmail.com")
        self.assertNotEqual(fakeuser.password, "password")
        self.assertTrue(fakeuser.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        """Test that a new user will not register if the username field is missing. Must include all fields: username, password, email, goal_cal, city, and state. Cannot miss state because form has select method."""
        nousername = User.signup(None, "nousername", "missing@username.com", 1200, "User", "NC")
        nousernameid = 123456789
        nousername.id = nousernameid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        """Test that a new user will not register if the email field is missing."""
        noemail = User.signup("zeroemail", "noemail", None, 1200, "Email", "NC")
        noemailid = 12345678
        noemail.id = noemailid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_goal_cal_signup(self):
        """Test that a new user will not register if the goal_cal field is missing."""
        nocal = User.signup("nocal", "zerocal", "missing@cal.com", 
        None, "User", "NC")
        nocalid = 1234567
        nocal.id = nocalid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_city_signup(self):
        """Test that a new user will not register if the city field is missing."""
        nocity = User.signup("nocity", "zerocity", "missing@city.com", 1200, None, "NC")
        nocityid = 123456
        nocity.id = nocityid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        """Test that a new user will not register if the password field is missing."""
        with self.assertRaises(ValueError) as context:
            User.signup("emptypw", "", "nopw@password.com", 1300, "Yes", "OK")

        with self.assertRaises(ValueError) as context:
            User.signup("forgotpwfield", None, "pw@forgot.com", 1234, "No", "CA")

# AUTHENTICATION TESTS

    def test_valid_authentication(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        noauth = User.authenticate(self.testuser1.username, "password")
        self.assertIsNotNone(noauth)
        self.assertEqual(noauth.id, self.testuser1id)

# FOLLOW TESTS

    def test_is_following(self):
        """Does is_following successfully detect when one user is following another user?"""
        self.testuser1.following.append(self.testuser2)
        db.session.commit()

        self.assertEqual(len(self.testuser2.following), 0)
        self.assertEqual(len(self.testuser1.following), 1)

        self.assertEqual(self.testuser1.following[0].id, self.testuser2.id)

        self.assertTrue(self.testuser1.is_following(self.testuser2))
        self.assertFalse(self.testuser2.is_following(self.testuser1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when one user is being followed by another user?"""
        self.testuser1.following.append(self.testuser2)
        db.session.commit()

        self.assertEqual(len(self.testuser2.followers), 1)
        self.assertEqual(len(self.testuser1.followers), 0)

        self.assertEqual(self.testuser2.followers[0].id, self.testuser1.id)

        self.assertTrue(self.testuser2.is_followed_by(self.testuser1))
        self.assertFalse(self.testuser1.is_followed_by(self.testuser2))