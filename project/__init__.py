from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

DB_NAME = 'db.db'
UPLOAD_FOLDER = os.path.abspath(os.path.join(basedir, 'static/img/'))
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
ADMIN_EMAIL = 'pablo@email.com'



def create_app():
    app = Flask(__name__, static_url_path='/static')
    # Instead of using config from an object, we define it here.
    app.config['SECRET_KEY'] = 'This is supposed to be secret.'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ADMIN_EMAIL'] = ADMIN_EMAIL

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    
    # Initialize third parties.
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


    # create database if it doesnt exist.
    update_database(app)

    # Add the blueprints.
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .muscle import muscle as muscle_blueprint
    app.register_blueprint(main_blueprint, url_prefix="")
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(muscle_blueprint, url_prefix='/muscle')

    
    return app

"""This initialize the database tables."""
def update_database(app):
    with app.app_context():
        db.create_all()
        print("Created database!")