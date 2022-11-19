from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "very 12/34%^&321 secret 843&*&9837t09 key ^(&*R@(*789y387"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
manager = LoginManager(app)

from sweater import models, roots

with app.app_context():
    db.create_all()
