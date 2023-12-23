from flask import request, render_template, redirect, url_for, flash, redirect
from flask_login import login_required, current_user
from . import forum
from .. import db
from ..models import Permission
from ..decorators import permission_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

@forum.route('')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('forum/index.html', posts=posts)


@forum.route('post/<int:id>/', methods=['GET', 'POST'])
def post_read(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()

    # POST request.
    if form.validate_on_submit() and current_user.can(Permission.COMMENT):
        comment = Comment(text=form.text.data, author=current_user._get_current_object(), post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!')
        return redirect(url_for('.post_read', id=id))

    # GET request.
    return render_template('forum/post.html', post=post, form=form)


@forum.route('/post/', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def post_create():
    form = PostForm()
    # POST request.
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    # GET request, returns the form.
    return render_template('forum/post_create.html', form=form)