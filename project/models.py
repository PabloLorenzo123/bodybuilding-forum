from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # Relationships.
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


"""Muscle building application."""
class Muscle(db.Model):
    __tablename__ = 'muscles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    image_name = db.Column(db.String(50), unique=True, nullable=True)
    description = db.Column(db.String(200), nullable=False)

    # Relationships.
    exercises = db.relationship('Exercise', backref='muscle', lazy='dynamic')

    def __repr__(self):
        return f"{self.name}"

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey('muscles.id', name='fk_exercise_muscle'))

    name = db.Column(db.String(50), unique=True)
    video_link = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(500))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author_name = db.Column(db.String(64))

    def __repr__(self):
        return f"{self.muscle}, {self.name}"



"""Finally, Flask-Login requires the application to designate a function to be invoked
when the extension needs to load a user from the database given its identifier. This
function is shown"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
