from flask import Blueprint
from flask_login import current_user

muscle = Blueprint('muscle', __name__)

from . import views