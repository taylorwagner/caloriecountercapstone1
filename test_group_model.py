"""Group and UserGroup model tests."""

from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Group, UserGroup
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///calcount_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class GroupModelTestCase(TestCase):
    """Test model for group."""