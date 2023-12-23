from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from ..models import User
from . import auth
from .. import db

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter_by(email=email).first():
            flash('Email is already in use', category='error')
        elif User.query.filter_by(username=username).first():
            flash('Username is already in use', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.')
        elif not password1 or not password2:
            flash('Fill all the fields.')
        else:
            new_user = User(email=email, username=username,
                            password=password1) # Password is generated automatically thanks to the property setter in models.py
            db.session.add(new_user)
            db.session.commit()
            flash(f"Welcome {username}!")
            login_user(new_user, remember=True)
            return redirect(url_for('main.index'))

    # GET request.
    return render_template('auth/signup.html')
    

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user, remember=True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash(f"Welcome back {user.username}!")
            return redirect(next)
        flash('Invalid username or password.')
    # GET request
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
