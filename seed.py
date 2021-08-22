"""Seed file to make sample data for calcountdb."""
from models import db, User, Group, UserGroup, Follows
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Group.query.delete()
UserGroup.query.delete()
Follows.query.delete()

# Add sample users
fake_u1 = User.signup(username="sanrpor", password="password", email="sanrpor@test.com", goal_cal=1800, city="Houston", state="TX")
fake_u1id = 553131
fake_u1.id = fake_u1id
fake_u2 = User.signup(username="leopeezy3", password="testpassword", email="lpp@gmail.com", goal_cal=1300, city="Lincoln", state="NE")
fake_u2id = 771010
fake_u2.id = fake_u2id
fake_u3 = User.signup(username="meglporter", password="testpwpw", email="fake@email.com", goal_cal=1000, city="Phoenix", state="AZ")
fake_u3id = 660101
fake_u3.id = fake_u3id
fake_u4 = User.signup(username="pauliefbaby", password="samplepassword", email="sports@nfl.com", goal_cal=3000, city="Austin", state="TX")
fake_u4id = 440202
fake_u4.id = fake_u4id

# Add new objects to sesion, so they'll persist
db.session.add_all([fake_u1, fake_u2, fake_u3, fake_u4])

# Commit
db.session.commit()

# Add sample groups
fake_g1 = Group(id=9988, name="#texashealthgroup", description="For users who currently live in Texas!")
fake_g2 = Group(id=9998, name="#youngandthriving", description="For users who are in their 20's")
fake_g3 = Group(id=9999, name="#classof99")
fake_g4 = Group(id=9888, name="#healthnewbies")

# Add new objects to session, so they'll persist
db.session.add_all([fake_g1, fake_g2, fake_g3, fake_g4])

# Commit
db.session.commit()

# Add sample users_groups
fake_ug1 = UserGroup(group_id=9988, user_id=553131)
fake_ug2 = UserGroup(group_id=9988, user_id=660101)
fake_ug3 = UserGroup(group_id=9998, user_id=553131)
fake_ug4 = UserGroup(group_id=9999, user_id=771010)

# Add new objects to session, so they'll persist
db.session.add_all([fake_ug1, fake_ug2, fake_ug3, fake_ug4])

# Commit
db.session.commit()

# Add sample follows
fake_f1 = Follows(id=99999, user_following_id=553131, user_followed_id=771010)
fake_f2 = Follows(id=99998, user_following_id=771010, user_followed_id=553131)
fake_f3 = Follows(id=99997, user_following_id=771010, user_followed_id=660101)
fake_f4 = Follows(id=99996, user_following_id=440202, user_followed_id=660101)

# Add new objects to session, so they'll persist
db.session.add_all([fake_f1, fake_f2, fake_f3, fake_f4])

# Commit
db.session.commit()