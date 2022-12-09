from flask_login import UserMixin

from sweater import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    second_name = db.Column(db.String(64))
    number = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    levelmas = db.Column(db.String)
    photo = db.Column(db.String)


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serv = db.Column(db.String(512))
    dat = db.Column(db.Date)
    time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('user.levelmas'), nullable=False)


class AccessRights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Access = db.Column(db.String, unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.Integer, db.ForeignKey('user.name'), nullable=False)
    text = db.Column(db.Text)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
