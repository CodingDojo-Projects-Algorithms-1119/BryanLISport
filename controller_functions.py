from flask import render_template, request, redirect, session	
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
        return render_template("dashboard.html", user=logged_in)

def user_info():
    return render_template("users.html")

def event_details():
    return render_template("event_details.html")

def search():
    return render_template("search.html")

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


#Simple Redirects

def logout():
    session.clear()
    return redirect("/")