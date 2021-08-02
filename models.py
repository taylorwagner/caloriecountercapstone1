"""SQLAlchemy models for Calorie Counter."""

from datetime import datetime, date
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text(min=8, max=30), nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        """Human readable representation of user table data."""
        return f"User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, email):
        """Sign up a user. Hashes password and adds user to the system."""
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=hashed_pw, email=email)

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with matching 'username' and 'password' combination."""
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Profile(db.Model):
    """A user's profile information."""

    __tablename__ = "profiles"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    gender = db.Column(db.Boolean)
    dob = db.Column(db.Datetime.Date)
    reason = db.Column(db.Text)
    goal_cal = db.Column(db.Integer, nullable=False)

class Group(db.Model):
    """Support groups for users to join"""

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

class UserGroup(db.Model):
    """Connection of a user <-> support group."""

    __tablename__ = "users_groups"

    group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete="cascade"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeginKey('user.id', ondelete="cascade"))

class Follow(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = "follows"

    user_following_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"), primary_key=True)
    user_followed_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"), primary_key=True)

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)