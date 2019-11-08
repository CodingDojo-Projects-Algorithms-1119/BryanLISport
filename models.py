from sqlalchemy.sql import func
from config import db

users_and_events = db.Table("users_and_events",
                   db.Column('user_id', db.Integer, db.ForeignKey("user.id"), primary_key=True),
                   db.Column('event_id', db.Integer, db.ForeignKey("event.id"), primary_key=True)) 

class User(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))
    events_user_attends = db.relationship("Event", secondary=users_and_events)
    created_at = db.Column(db.DateTime, server_default=func.now())   
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(55))
    info = db.Column(db.String(500))
    participants = db.Column(db.Integer)
    location = db.Column(db.String(100))
    users_attending_event = db.relationship("User", secondary=users_and_events)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], backref="user_message", cascade="all")
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    event = db.relationship("Event", foreign_keys=[event_id], backref="event_messages", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())