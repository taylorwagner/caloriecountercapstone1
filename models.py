"""SQLAlchemy models for Calorie Counter."""

import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follow(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = "follows"

    user_following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    user_followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)

    def __repr__(self):
        """Human readable representation of follow table data."""
        return f"<Follow: user_following_id={self.user_following_id}, user_followed_id={self.user_followed_id}>"


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    goal_cal = db.Column(db.Integer, nullable=False)

    comments = db.relationship('Comment', backref="user", cascade="all, delete-orphan")

    profiles = db.relationship('Profile', backref="user", cascade="all, delete-orphan")

    following = db.relationship("User", secondary="follows", primaryjoin=(Follow.user_following_id == id), secondaryjoin=(Follow.user_followed_id == id))

    followers = db.relationship("User", secondary="follows", primaryjoin=(Follow.user_followed_id == id), secondaryjoin=(Follow.user_following_id == id))

    groups = db.relationship("Group", secondary="users_groups", backref="users")

    def __repr__(self):
        """Human readable representation of user table data."""
        return f"<User #{self.id}: {self.username}, {self.email}, goal_calories={self.goal_cal}>"

    @classmethod
    def signup(cls, username, password, email, goal_cal):
        """Sign up a user. Hashes password and adds user to the system."""
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=hashed_pw, email=email, goal_cal=goal_cal)

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
    state = db.Column(db.String(2))
    gender = db.Column(db.Boolean)
    # dob = db.Column(db.DateTime, default=datetime.date())
    reason = db.Column(db.Text)

    # def __repr__(self):
    #     """Human readable representation of profile table data."""
    #     return f"<Profile: user={self.user_id} name={self.first_name} {self.last_name} location={self.city}, {self.state} gender={self.gender} dob={self.dob} reason='{self.reason}'>"

class Group(db.Model):
    """Support groups for users to join"""

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        """Human readable representation of group table data."""
        return f"<Group: id={self.id} name={self.name} desc='{self.description}'>"

class UserGroup(db.Model):
    """Connection of a user <-> support group."""

    __tablename__ = "users_groups"

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete="cascade"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

    def __repr__(self):
        """Human readable representation of user_group table data."""
        return f"<UserGroup: group_id={self.group_id} user_id={self.user_id}>"


class Comment(db.Model):
    """Users can leave comments for themselves, users he/she follows, and groups he/she is in."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    @property
    def readable_date(self):
        """Return formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        """Human readable representation of user table data."""
        return f"<Comment: id={self.id} text={self.text} timestamp={self.created_at}>"

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)