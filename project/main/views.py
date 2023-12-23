from . import main
from flask import request, render_template, redirect, url_for

@main.route("/")
def index():
    return render_template("index.html")