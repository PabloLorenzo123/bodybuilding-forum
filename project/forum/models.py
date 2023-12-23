from .. import db
from datetime import datetime


class Post(db.Model):
 __tablename__ = 'posts'
 id = db.Column(db.Integer, primary_key=True)
 title = db.Column(db.String(50))
 body = db.Column(db.Text)
 timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
 author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

 # Relationships.
 comments = db.Relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
 __tablename__ = 'comments'
 id = db.Column(db.Integer, primary_key=True)
 text = db.Column(db.Text())
 author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
 timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

 post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))