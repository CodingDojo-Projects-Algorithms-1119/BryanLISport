from flask import Flask, render_template, request, redirect, flash, session
import re
from sqlalchemy.sql import func
from config import db, bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

users_and_events = db.Table("users_and_events",
                   db.Column('user_id', db.Integer, db.ForeignKey("user.id"), primary_key=True),
                   db.Column('event_id', db.Integer, db.ForeignKey("event.id"), primary_key=True)) 

class User(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))
    email = db.Column(db.String(55))
    password = db.Column(db.Text(55))
    events_user_attends = db.relationship("Event", secondary=users_and_events, lazy="dynamic")
    created_at = db.Column(db.DateTime, server_default=func.now())   
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_registration(cls, user_registration):

        is_valid = True

        if len(user_registration["first_name"]) < 1:
            is_valid = False
            flash("First name can not be blank", "error")
        
        if len(user_registration["last_name"]) < 1:
            is_valid = False
            flash("Last name can not be blank", "error")

        if len(user_registration["email"]) < 1:
            is_valid = False
            flash("Email can not be blank")

        if not EMAIL_REGEX.match(user_registration["email"]):
            flash("Invalid email address", "error" )

        if len(user_registration["password"]) < 5:
            is_valid = False
            flash("Password must be at least 5 characters", "error")

        if len(user_registration["password"]) > 55:
            is_valid = False
            flash("Password can not be more than 45 characters", "error")

        if len(user_registration["conf_pass"]) < 1:
            is_valid = False
            flash("Confirm Password can not be blank", "error")

        if user_registration["conf_pass"] != user_registration["password"]:
            is_valid = False
            flash("Passwords must match", "error")
        
        return is_valid

    @classmethod
    def create_user(cls, user_data):
        pw_hash = bcrypt.generate_password_hash(user_data['password']).decode("utf-8")
        create_user = cls(first_name = user_data["first_name"], last_name = user_data["last_name"], email = user_data["email"], password = pw_hash)
        db.session.add(create_user)
        db.session.commit()
        return create_user

    @classmethod
    def login_validation(cls, login_info):
        is_valid = True

        if len(login_info['lemail']) < 1 or not EMAIL_REGEX.match(login_info["lemail"]):
            is_valid = False
            flash("Please enter your email")

        if len(login_info['lpassword']) < 5: 
            is_valid = False
            flash("Please enter your password")

        if not is_valid:
            return is_valid

        user = cls.query.filter_by(email=login_info["lemail"]).first()

        if user:
            if bcrypt.check_password_hash(user.password, login_info["lpassword"]):
                session["user_id"] = user.id
                return is_valid

            else:
                is_valid = False
                flash("Invalid Credentials")
                return is_valid
        else:
            is_valid = False
            flash("User not Found")
            return is_valid

        return is_valid

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(55))
    time = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    event_details = db.Column(db.String(250))
    users_attending_event = db.relationship("User", secondary=users_and_events)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], backref=("user_message"), cascade="all")
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    event = db.relationship("Event", foreign_keys=[event_id], backref="event_messages", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def post_message(cls, form_message):
        is_valid = True

        if len(form_message["create_message"]) > 150:
            is_valid = False
            flash("Max character count is 150")
            return is_valid
        else:
            message_being_posted = Message(content = form_message["create_message"], user_id = session["user_id"], event_id = form_message["event_id"])
            db.session.add(message_being_posted)
            db.session.commit()
            return message_being_posted, is_valid