from .. import db


class PaperSaved(db.Model):
    __tablename__ = 'PapersSaved'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Details about the paper.
    date = db.Column(db.DateTime())
    title = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    pmid = db.Column(db.Integer)

    abstract = db.Column(db.Text())
    results = db.Column(db.Text())
    conclusions = db.Column(db.Text())
