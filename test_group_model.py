"""Group, UserGroup, and Food model tests."""

from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Group, UserGroup, Food
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///calcount_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class GroupModelTestCase(TestCase):
    """Test model for group."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.testuserid = 2012
        testuser = User.signup("testuser", "fakepassword", "emailemail@email.com", 2012, "Bronx", "NY")
        testuser.id = self.testuserid
        db.session.commit()

        self.testuser = User.query.get(self.testuserid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_group_model(self):
        """Does basic model work?"""
        testgroup = Group(name="#farmers", description="For people who live on the farm or love to farm!")

        testgroup2 = Group(name="#nodescription")

        db.session.add_all([testgroup, testgroup2])
        db.session.commit()

        self.assertIsNotNone(testgroup)
        self.assertEqual(testgroup.name, "#farmers")
        self.assertEqual(testgroup.description, "For people who live on the farm or love to farm!")

        self.assertIsNotNone(testgroup2)
        self.assertEqual(testgroup2.name, "#nodescription")
        self.assertIsNone(testgroup2.description, None)

    def test_user_group_model(self):
        """Test to verify that users are being connected to groups via UserGroup."""
        group1 = Group(name="#ilovetosing")
        group1id = 9090
        group1.id = group1id

        db.session.add(group1)
        db.session.commit()

        testusergroup = UserGroup(group_id=group1.id, user_id=self.testuserid)

        db.session.add(testusergroup)
        db.session.commit()

        usergroupcount = UserGroup.query.all()

        self.assertIsNotNone(testusergroup)
        self.assertEqual(testusergroup.group_id, 9090)
        self.assertEqual(testusergroup.user_id, 2012)
        self.assertEqual(len(usergroupcount), 1)

    def test_food_model(self):
        """Test to verify that users are being connected to a food input via Food."""
        fakefood = Food(user_id=self.testuserid, date="09-17-2021", food="chicken and rice casserole", calories="1234")

        db.session.add(fakefood)
        db.session.commit()

        self.assertIsNotNone(fakefood)
        self.assertEqual(fakefood.user_id, 2012)