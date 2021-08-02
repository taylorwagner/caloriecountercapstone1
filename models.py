"""SQLAlchemy models for Calorie Counter."""

from datetime import datetime
from re import U
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
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

        u = User(username=username, password=hashed_pw, email=email)

        db.session.add(u)
        return U
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with matching 'username' and 'password' combination."""
        u = cls.query.filter_by(username=username).first()

        if u:
            is_auth = bcrypt.check_password_hash(u.password, password)
            if is_auth:
                return U

        return False

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)