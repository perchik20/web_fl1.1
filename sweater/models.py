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


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serv = db.Column(db.String(512))
    dat = db.Column(db.String)
    time = db.Column(db.String)
    id_user = db.Column(db.Integer, nullable=False)
    id_master = db.Column(db.Integer, nullable=False)


class AccessRights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Access = db.Column(db.String, unique=True)


class IdAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    idAccess = db.Column(db.Integer)


class AllServ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    that = db.Column(db.String)
    name_serv = db.Column(db.String, unique=True)
    price = db.Column(db.Integer)
    time = db.Column(db.String)
    level_mas = db.Column(db.Integer)


class Reviews (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    review = db.Column(db.Text)


class LevelMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)


class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_mas = db.Column(db.Integer, primary_key=True)
    time0 = db.Column(db.String, default='10:00')
    time1 = db.Column(db.String, default='11:00')
    time2 = db.Column(db.String, default='12:00')
    time3 = db.Column(db.String, default='13:00')
    time4 = db.Column(db.String, default='14:00')
    time5 = db.Column(db.String, default='15:00')
    time6 = db.Column(db.String, default='16:00')
    time7 = db.Column(db.String, default='17:00')
    time8 = db.Column(db.String, default='18:00')
    time9 = db.Column(db.String, default='19:00')
    time10 = db.Column(db.String, default='20:00')
    time11 = db.Column(db.String, default='21:00')
    time12 = db.Column(db.String, default='21:00')



@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
