from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = TextAreaField("title", validators=[DataRequired(), Length(5, 50)])
    body = TextAreaField("What topic would you like to discuss?", validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text = TextAreaField("What do you think about this?", validators=[DataRequired()])
    submit = SubmitField('Comment')