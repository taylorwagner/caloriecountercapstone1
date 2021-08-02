"""Calorie Counter Flask App."""
import os
from flask import Flask
import flask_sqlalchemy
from models import db, connect_db, User, Profile, Group, UserGroup, Follow, Comment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///calcount'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)