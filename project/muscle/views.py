from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
import urllib.request
import os
from werkzeug.utils import secure_filename

from . import muscle
from . import db
from ..models import Muscle, Exercise
from .. import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

@muscle.context_processor
def inject_user():
    return dict(user=current_user or None)
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@muscle.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_muscle(id):
    muscle = Muscle.query.get(id)
    muscle_img_url = url_for('static', filename=muscle.image_name)

    if muscle is None:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name')
        summary = request.form.get('summary')

        if name:
            muscle.name = name
        if summary:
            muscle.summary = summary

        """This ain't working yet."""
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
        return redirect(request.url)
    # GET method.
    return render_template("muscle/update_muscle.html", muscle=muscle, muscle_img_url=muscle_img_url)


@muscle.route("/detail/<string:muscle>")
def muscle_detail(muscle):
    muscle = Muscle.query.filter_by(name=muscle).first()
    exercises = muscle.exercises.all()
    if muscle is None:
        abort(404)
    
    return render_template('muscle/muscle_detail.html', muscle=muscle, exercises=exercises)


@muscle.route("/exercises/add/<string:muscle>/", methods=['GET', 'POST'])
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


@muscle.route("/exercises/<string:muscle>/<string:name>")
def exercise_detail(muscle, name):
    muscle = Muscle.query.filter_by(name=muscle).first()

    if muscle is None:
        return abort(404)
    
    exercise = Exercise.query.filter_by(muscle=muscle, name=name).first()

    if exercise:
        return render_template('muscle/exercise_detail.html', exercise=exercise)
    
    return abort(404)

"""Edit, and delete exercise view is missing."""