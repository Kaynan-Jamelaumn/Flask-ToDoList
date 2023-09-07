from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
# from sqlalchemy import event
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tasks = db.relationship('Task')

    def __repr__(self):
        return f'{self.id} {self.email} {self.name}'
    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    text = db.Column(db.String(1000))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    public = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user_id is the name of the table and the field

# @event.listens_for(Task, 'before_update')
# def before_update_listener(mapper, connection, target):
#     # Set updated_at to the current timestamp
#     target.updated_at = func.now()

        