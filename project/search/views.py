from flask import request, redirect, url_for, render_template, flash, abort
from flask_login import current_user, login_required
from . import search
from .models import PaperSaved
from .search_json import create_table, esummary
from .. import db
from ..auth.views import login


@search.route('/', methods=['GET', 'POST'])
def search_results():
    # The post request should all the paper to the user's account.
    if request.method == 'POST':
        # If a user not authenticated tries to save the paper, he will be redirected to login.
        if not current_user.is_authenticated:
            flash('You need to be logged in, to save articles.', category='error')
            return redirect(url_for('auth.login'))
        
        pmid = str(request.form.get('pmid'))

        if not pmid:
            return flash('You need to select before submiting.')
        
        esm = esummary(pmid)

        # Check if its already saved.
        if PaperSaved.query.filter_by(pmid=pmid, user_id=current_user.id).first():
            return flash('You already have this article saved.')
        else:
            paper_saved = PaperSaved(
                user_id=current_user.id,
                date = esm['date'],
                title = esm['title'],
                authors = esm['authors'],
                pmid = esm['id'],
                abstract = esm['study']['abstract'],
                results = esm['study']['results'],
                conclusions = esm['study']['conclusion'],
                )
            db.session.add(paper_saved)
            db.session.commit()
            flash('This paper has been saved.')
            return redirect(url_for('search.my_papers'))

        
    # GET method, this show the results.
    q = request.args.get('q')
    if not q:
        flash('You need to type something in the search bar.')
        return
    else:
        try:
            results = create_table(q)
        except:
            return abort(429)
        
        papers_saved = []
        if current_user.is_authenticated:
            papers_saved = [str(paper.pmid) for paper in current_user.papers_saved]
        return render_template('search/results.html', results=results, papers_saved=papers_saved)


"""This view allow users to add the study into their account."""
@search.route('/my_saved_papers/', methods=['GET', 'POST'])
@login_required
def my_papers():
    # POST will handle deletion of saved articles.
    if request.method == 'POST':
        # If a user not authenticated tries to save the paper, he will be redirected to login.
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        pmid = str(request.form.get('pmid'))

        if not pmid:
            return flash('You need to select before submiting.')
        
        paper_saved = PaperSaved.query.filter_by(pmid=pmid, user_id=current_user.id).first()
        if paper_saved:
            db.session.delete(paper_saved)
            db.session.commit()
            flash('This paper has been removed.')
            return redirect(url_for('search.my_papers'))
    # GET request.
    saved_articles = PaperSaved.query.filter_by(user_id=current_user.id).all()
    return render_template('search/my_papers.html', saved_articles=saved_articles)