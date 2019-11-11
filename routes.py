from config import app
from controller_functions import login_register, dashboard, user_info, event_details, search, register_new_user, logout, login, join_event

# Render Templates

app.add_url_rule("/", view_func=login_register)

app.add_url_rule("/dashboard", view_func=dashboard)

app.add_url_rule("/user_info", view_func=user_info)

app.add_url_rule("/event_details/<event_id>", view_func=event_details)

app.add_url_rule("/search", view_func=search)

# Form Redirects

app.add_url_rule("/register", view_func=register_new_user, methods=["POST"])

app.add_url_rule("/login", view_func=login, methods=["POST"])

app.add_url_rule("/join_event/<event_id>", view_func=join_event)

# Simple Redirects

app.add_url_rule("/logout", view_func=logout)


