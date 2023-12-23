from flask import Blueprint
from flask_login import current_user
from ..models import Permission
from ..muscle.models import Muscle

main = Blueprint('main', __name__)

from . import views

@main.app_context_processor
def inject_user():
    return dict(user=current_user or None)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

@main.app_context_processor
def inject_muscles():
    return dict(muscles=Muscle.query.all())