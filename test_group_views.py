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

    def test_all_groups(self):
        """Test the all groups page is displaying all groups in db."""
        testgroup = Group(id=999999999, name="testgroup")
        testgroup2 = Group(id=999999998, name="testgroup2", description="test group description")

        db.session.add_all([testgroup, testgroup2])
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            testgroup = Group.query.get(999999999)
            testgroup2 = Group.query.get(999999998)

            res = c.get("/groups")
            self.assertIn("testgroup", str(res.data))
            self.assertIn("testgroup2", str(res.data))
            self.assertIn(testgroup2.name, str(res.data))
            self.assertNotIn("nogroup", str(res.data))

    # def test_new_group(self):
    #     """Test that a new group can be added with the form."""
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         res = c.post("/groups/new", data={"name": "TESTING GROUP!!!!"}, follow_redirects=True)

    #         self.assertEqual(res.status_code, 302)

    #         group = Group.query.one()
    #         self.assertEqual(group.name, "TESTING GROUP!!!!")

    def test_show_group(self):
        """Test to detect that when an authorized user clicks on a valid group page, the group shows along with description (if valid) and included users (if valid)."""
        testgroupdesc = Group(id=999999997, name="testtesttestgroup", description="test group including a description")

        db.session.add(testgroupdesc)
        db.session.commit()

        testusergroup = UserGroup(id=99999, group_id=999999997, user_id=self.testuser.id)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            group = Group.query.get(999999997)

            res = c.get(f"/groups/{group.id}")

            self.assertEqual(res.status_code, 200)
            self.assertIn(group.name, str(res.data)) 

    def test_invalid_show_group(self):
        """Test that 404 page/message will kick in for an invalid group id"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get("/groups/9ujh8y689")

            self.assertEqual(res.status_code, 404)