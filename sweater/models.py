from flask_login import UserMixin

from sweater import db, manager


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    second_name = db.Column(db.String(64))
    number = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    master_level_id = db.Column(db.Integer, db.ForeignKey('level_master.id'), nullable=True)
    photo = db.Column(db.String)


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access = db.Column(db.String, unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class LevelMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    duration = db.Column(db.Time)
    master_level_id = db.Column(db.Integer, db.ForeignKey('level_master.id'), nullable=False)


class Reviews (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
