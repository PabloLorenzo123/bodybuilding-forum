from flask import Blueprint

muscle = Blueprint('muscle', __name__)

from .. import db
from . import views