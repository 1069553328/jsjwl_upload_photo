#encoding: utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    teamname = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(50), nullable=False)
    stuID = db.Column(db.String(11),nullable=False)
    password = db.Column(db.String(100), nullable=False)
    proclass = db.Column(db.String(100), nullable=False)

class Submit_file(db.Model):
    __tablename__ = 'submit_file'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    filepath = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User',backref=db.backref('submit_files'))
