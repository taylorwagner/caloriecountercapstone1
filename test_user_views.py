"""User and Follows view tests."""

from unittest import TestCase
from models import db, connect_db, User, Follows
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

    def test_show_account(self):
        """Test feature that displays a page with current user's account information."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get(f'/account/{self.testuser_id}')

            self.assertIn('Do you want to edit your account?', str(res.data))
            self.assertNotIn('user1@gmail.com', str(res.data))

    def test_edit_account(self):
        """Test feature that allows a current user's account information to be edited."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.post(f"/account/{self.testuser_id}/edit", follow_redirects=True)

            self.assertEqual(res.status_code, 200)

    def test_delete_account(self):
        """Test feature that allows a current user's account information to be deleted."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.post("/account/delete", follow_redirects=True)

            self.assertEqual(res.status_code, 200)

            u = User.query.get(self.testuser.id)
            self.assertIsNone(u)

# FOLLOW TESTS

    def setup_followers(self):
        """Create test client, add sample data for followers"""
        f1 = Follows(user_following_id=self.testuser_id, user_followed_id=self.user1_id)
        f2 = Follows(user_following_id=self.testuser_id, user_followed_id=self.user2_id)
        f3 = Follows(user_following_id=self.user1_id, user_followed_id=self.testuser_id)

        db.session.add_all([f1,f2,f3])
        db.session.commit()

    def test_show_following(self):
        """Test show_following to see if followed users are detected"""
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            res = c.get(f"/account/{self.testuser_id}/following")

            self.assertEqual(res.status_code, 200)

            self.assertIn("user1", str(res.data))
            self.assertIn("user2", str(res.data))
            self.assertNotIn("user3", str(res.data))

    def test_show_followers(self):
        """Test users_followers to see if users that are following are detected"""
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            res = c.get(f"/account/{self.testuser_id}/followers")

            self.assertEqual(res.status_code, 200)

            self.assertIn("user1", str(res.data))
            self.assertNotIn("user2", str(res.data))
            self.assertNotIn("user3", str(res.data))

    def test_unauthorized_following_page_access(self):
        """Test users_following unauthorized access feature for a user who is not the current logged in user"""
        self.setup_followers()
        with self.client as c:
            
            res = c.get(f"/account/{self.testuser_id}/following", follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn("user1", str(res.data))
            self.assertIn("Access unauthorized", str(res.data))

    def test_unauthorized_followers_page_access(self):
        """Test users_followers unauthorized access feature for a user who is not the current logged in user"""
        self.setup_followers()
        with self.client as c:
            
            res = c.get(f"/account/{self.testuser_id}/followers", follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn("user1", str(res.data))
            self.assertIn("Access unauthorized", str(res.data))