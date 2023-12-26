import os
# Third parties.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()

login_manager.login_view = 'auth.login'

DB_NAME = 'database.sqlite'
ADMIN_EMAIL = 'pablo@email.com'


def create_app():
    app = Flask(__name__, static_url_path='/static')
    # Instead of using config from an object, we define it here.
    app.config['SECRET_KEY'] = 'This is supposed to be secret.'
    app.config['ADMIN_EMAIL'] = ADMIN_EMAIL

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)
    
    # Initialize third parties.
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # create database if it doesnt exist.
    update_database(app)

    # Add the blueprints.
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .muscle import muscle as muscle_blueprint
    from .forum import forum as forum_blueprint
    from .search import search as search_blueprint
    app.register_blueprint(main_blueprint, url_prefix="")
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(muscle_blueprint, url_prefix='/muscle')
    app.register_blueprint(forum_blueprint, url_prefix='/forum')
    app.register_blueprint(search_blueprint, url_prefix='/search')
    
    return app

"""This initialize the database tables."""
def update_database(app):
    with app.app_context():
        db.create_all()