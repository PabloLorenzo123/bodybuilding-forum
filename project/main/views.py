from . import main
from flask import request, render_template, redirect, url_for, flash
from ..auth.models import User, Role
from .. import db

# Home page
@main.route("/")
def index():
    return render_template("index.html")
