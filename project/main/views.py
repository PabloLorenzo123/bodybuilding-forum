from . import main
from flask import request, render_template

# Home page
@main.route("/")
def index():
    return render_template("index.html")
