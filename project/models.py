from . import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import ADMIN_EMAIL


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    # Relationships.
    users = db.relationship('User', backref='role', lazy='dynamic')

    # To avoid geeting permissions == None by default.
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    def reset_permissions(self):
        self.permissions = 0
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    """This method creates all the roles and save them in the database."""
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                        Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
            Permission.WRITE, Permission.MODERATE,
            Permission.ADMIN],
            }
        
        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()

            for perm in roles[r]:
                role.add_permission(perm)
            # If its the default role, this will be set to True. In this case User.
            role.default = (role.name == default_role)
            db.session.add(role)
        
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == ADMIN_EMAIL:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_admin(self):
        return self.can(Permission.ADMIN)
    

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
    
"""For added convenience, a custom AnonymousUser class that implements the can()
and is_administrator() methods is created as well. This will enable the application
to freely call current_user.can() and current_user.is_administrator() without
having to check whether the user is logged in first. """
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


"""Finally, Flask-Login requires the application to designate a function to be invoked
when the extension needs to load a user from the database given its identifier. This
function is shown"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




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




