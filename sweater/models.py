from flask_login import UserMixin

from sweater import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    second_name = db.Column(db.String(64))
    number = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serv = db.Column(db.String(100))
    time = db.Column(db.String, unique=True)
    id_user = db.Column(db.Integer, nullable=False)
    id_master = db.Column(db.Integer, nullable=False)


class Masters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    master = db.Column(db.String(100), nullable=False, unique=True)
    serv1 = db.Column(db.String, nullable=False)
    serv2 = db.Column(db.String, nullable=False)


class AccessRights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    Access = db.Column(db.String, unique=True)


class IdAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    idAccess = db.Column(db.Integer)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time9 = db.Column(db.DateTime)
    time10 = db.Column(db.DateTime)
    time11 = db.Column(db.DateTime)
    time12 = db.Column(db.DateTime)
    time13 = db.Column(db.DateTime)
    time14 = db.Column(db.DateTime)
    time15 = db.Column(db.DateTime)


class AllServ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.Integer)
    that = db.Column(db.String)
    name_serv = db.Column(db.String, unique=True)
    price = db.Column(db.Integer)
    time = db.Column(db.String)


class Reviews (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    review = db.Column(db.Text)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
