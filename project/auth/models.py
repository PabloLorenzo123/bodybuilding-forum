from .. import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager
from .. import ADMIN_EMAIL
from datetime import datetime


class Permission:
    WRITE = 1
    COMMENT = 2
    ADMIN = 4

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
        return self.permissions & perm == perm # Bit wise operation.
    
    """This method creates all the roles and save them in the database."""
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT, Permission.WRITE],
            'Administrator': [Permission.COMMENT, Permission.WRITE,
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

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow) # datetime.utcnow is missing the () at the end. This is because the default argument in db.Column() can take a function as a value. 
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    password_hash = db.Column(db.String(128))

    # Relationships.
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    papers_saved = db.relationship('PaperSaved', lazy='dynamic', cascade='all, delete-orphan')

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
    
    # To keep the last visit date for all users updated, the ping() method must be called each time a request from a user is received. 
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    

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
    
    def is_admin(self):
        return False


"""Finally, Flask-Login requires the application to designate a function to be invoked
when the extension needs to load a user from the database given its identifier. This
function is shown"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser
