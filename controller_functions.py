from flask import render_template, request, redirect	
from config import app, db, migrate
from models import User, Event, Message