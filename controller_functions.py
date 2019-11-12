from flask import render_template, request, redirect, session
from sqlalchemy import func	
from config import app, db, migrate
from models import User, Event, Message, users_and_events

app.secret_key = ("secret")

# Render Templates

def login_register():
    return render_template("log_reg.html")

def dashboard():
    if "user_id" not in session:
        return redirect ("/")

    else:
        logged_in = User.query.get(session["user_id"])
        events = logged_in.events_user_attends.all()
        return render_template("dashboard.html", user=logged_in, users_events = events)

def user_info():
    return render_template("users.html")

def event_details(event_id):
    details = Event.query.get(event_id)
    posted_messages = Message.query.filter_by(event_id = event_id, user_id=session["user_id"])
    return render_template("event_details.html", information=details, posts=posted_messages)

def search():
    display_info = Event.query.order_by(Event.time).all()
    return render_template("search.html", all_events = display_info)

# Form Redirects

def register_new_user():
    validation_check = User.validate_registration(request.form)
    if not validation_check:
        return redirect("/")
    
    else:
        new_user = User.create_user(request.form)
        session["user_id"] = new_user.id
        print("code ran")
        return redirect ("/dashboard")

def login():
    login_check = User.login_validation(request.form)
    if login_check:
        return redirect("/dashboard")
    else: 
        return redirect("/")

def join_event(event_id):
    user_joining_event = User.query.get(session["user_id"])
    event_being_joined = Event.query.get(event_id)
    user_joining_event.events_user_attends.append(event_being_joined)
    db.session.commit()
    return redirect("/event_details/{}".format(event_id))

def post_event_message(event_id):
    post_event_message = Message.post_message(request.form)

    if not post_event_message:
        return redirect("/event_details/<event_id>")
    else:
        return redirect("/event_details/{}".format(event_id))


#Simple Redirects

def logout():
    session.clear()
    return redirect("/")