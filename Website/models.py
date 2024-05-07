from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class file(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    subject = db.Column(db.String(20))
    path = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name =  db.Column(db.String(40))
    roll =  db.Column(db.Integer, unique=True)
    course = db.Column(db.String(50))
    notes = db.relationship('Note')
    files = db.relationship('file')
    assigns = db.relationship('assigns')
    news = db.relationship('news')


class ClassSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(40),nullable=False)
    instructor = db.Column(db.String(40),nullable=False)
    date =  db.Column(db.Date, nullable=False)
    time =  db.Column(db.Time,nullable=False)




class assigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(2000))  
    subject = db.Column(db.String(30))
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class news(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

