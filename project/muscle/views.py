from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
import urllib.request
import os
from werkzeug.utils import secure_filename

from . import muscle
from . import db
from ..models import Muscle, MuscleDivision, Exercise
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


@muscle.route("/detail/<string:name>")
def muscle_detail(name):
    muscle = Muscle.query.filter_by(name=name).first()

    if muscle is None:
        abort(404)

    muscle_img_url = url_for('static', filename=muscle.image_name)
    
    return render_template('muscle/muscle_detail.html', muscle=muscle)


@muscle.route("/exercises/add/<string:name>")
def add_exercise(name):
    muscle = Muscle.query.filter_by(name=name).first()
    if muscle is None:
        abort(404)
    
    