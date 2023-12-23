from . import main
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Role
from .. import db
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm


@main.route("/")
def index():
    return render_template("index.html")

@main.route('/user/<username>')
def user_detail(username):
    user_profile = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user_profile=user_profile)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def user_update():
    form = EditProfileForm()
    # POST request.
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(f'{current_user.name} your profile has been updated.')
        return redirect(url_for('main.user_detail', username=current_user.username))
    # GET request.
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    # POST request.
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    # GET request.
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)