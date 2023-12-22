from . import main
from flask import request, render_template, redirect, url_for
from flask_login import current_user

@main.context_processor
def inject_user():
    return dict(user=current_user or None)

@main.route("/")
def index():
    return render_template("index.html")