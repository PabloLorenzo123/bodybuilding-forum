from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
import urllib.request
import os
from werkzeug.utils import secure_filename

from . import muscle
from .. import db
from .models import Muscle, Exercise
from ..decorators import admin_required
from .. import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@muscle.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def muscle_update(id):
    muscle = Muscle.query.get(id)

    if muscle is None:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name').lower()
        summary = request.form.get('summary')
        file = request.files['file']

        if name:
            muscle.name = name
        if summary:
            muscle.description = summary

        """This ain't working yet."""
        if file:
            if 'file' in request.files:
                print("there's file")
                file = request.files['file']
                if file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    muscle.image = f'img/{filename}' 
                    print("saving file")
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')

        # Update database.
        db.session.add(muscle)
        db.session.commit()
        return redirect(url_for('muscle.muscle_detail', muscle=muscle.name))
    # GET method.
    return render_template("muscle/update_muscle.html", muscle=muscle)


"""See muscle info page"""
@muscle.route("/detail/<string:muscle>")
def muscle_detail(muscle):
    muscle = Muscle.query.filter_by(name=muscle.lower()).first_or_404()

    exercises = muscle.exercises.all()
    
    return render_template('muscle/muscle_detail.html', muscle=muscle, exercises=exercises)


"""See the info of an exercise"""
@muscle.route("/exercises/<string:muscle>/<string:name>")
def exercise_detail(muscle, name):
    muscle = Muscle.query.filter_by(name=muscle).first()

    if muscle is None:
        return abort(404)
    
    exercise = Exercise.query.filter_by(muscle=muscle, name=name).first()

    if exercise:
        return render_template('muscle/exercise_detail.html', exercise=exercise)
    
    return abort(404)


"""Add an exercise to a muscle group."""
@muscle.route("/exercises/add/<string:muscle>/", methods=['GET', 'POST'])
@login_required
@admin_required
def create_exercise(muscle):
    muscle = Muscle.query.filter_by(name=muscle).first()

    if muscle is None:
        abort(404)
    # POST request.
    if request.method == 'POST':
        title = request.form.get('title')
        video_link = request.form.get('video_link')
        description = request.form.get('description')

        if not title:
            flash('Add a name to the exercise.')
        elif not description:
            flash("Add a description.")
        else:
            new_exercise = Exercise(name=title, video_link=video_link, muscle_id=muscle.id,
                                    description=description, author_id=current_user.id,
                                    author_name=current_user.username)
            db.session.add(new_exercise)
            db.session.commit()

            return redirect(url_for('muscle.muscle_detail',muscle=muscle.name))
    
    # GET Method, returns form.
    return render_template('muscle/create_exercise.html', muscle=muscle)




"""Edit, and delete exercise view is missing."""