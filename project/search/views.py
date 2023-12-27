from flask import request, redirect, url_for, render_template, flash, abort
from flask_login import current_user, login_required
from . import search
from .models import PaperSaved
from .search_json import create_table, esummary
from .. import db
from ..helpers import apology


@search.route('/', methods=['GET', 'POST'])
def search_results():
    # The post request should all the paper to the user's account.
    if request.method == 'POST':
        # If a user not authenticated tries to save the paper, he will be redirected to login.
        if not current_user.is_authenticated:
            flash('You need to be logged in, to save articles.', category='error')
            return redirect(url_for('auth.login'))
        
        pmids = request.form.getlist('pmid')

        if not pmids:
            return apology('You need to select at least an article.')
        
        for pmid in pmids:

            # Check if its already saved.
            if PaperSaved.query.filter_by(pmid=pmid, user_id=current_user.id).first():
                return apology('You already have one of these articles saved.')
            else:
                esm = esummary(pmid) # We need to do this, so the user cant change the HTML code and affect the articles saved.
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
        
        if len(pmids) > 1:
            flash('The selected articles have been saved.')
            return redirect(url_for('search.my_articles'))
        else:
            flash('This article has been saved.')
            return redirect(url_for('search.my_articles'))
        
    # GET method, this show the results.
    q = request.args.get('q')
    if not q:
        return apology('You need to type something in the search bar.')
    else:
        try:
            results = create_table(q)
        except:
            abort(429)
        
        articles_saved = []
        if current_user.is_authenticated:
            articles_saved = [str(paper.pmid) for paper in current_user.papers_saved]
        return render_template('search/search_results.html', results=results, articles_saved=articles_saved)


"""This view allow users to add the study into their account."""
@search.route('/my_saved_papers/', methods=['GET', 'POST'])
@login_required
def my_articles():
    # POST will handle deletion of saved articles.
    if request.method == 'POST':
        # If a user not authenticated tries to save the paper, he will be redirected to login.
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        pmids = request.form.getlist('pmid')

        if not pmids:
            return apology('You need to select at least one article to delete.')
        
        for pmid in pmids:
            article_saved = PaperSaved.query.filter_by(pmid=pmid, user_id=current_user.id).first()
            if article_saved:
                db.session.delete(article_saved)
                db.session.commit()
        
        if len(pmids) > 1:
            flash('The selected articles have been removed.')
        else:
            flash('This article has been removed.')
        return redirect(url_for('search.my_articles'))
    # GET request.
    saved_articles = PaperSaved.query.filter_by(user_id=current_user.id).all()
    return render_template('search/my_articles.html', saved_articles=saved_articles)