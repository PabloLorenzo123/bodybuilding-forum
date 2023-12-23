from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
   
   email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
   username = StringField('Username', validators=[ DataRequired(), Length(1, 64), 
                                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                         'Usernames must have only letters, numbers, dots or ''underscores')])
   role = SelectField('Role', coerce=int) # so that the field values are stored as integers instead of the default, which is strings.
   name = StringField('Real name', validators=[Length(0, 64)])
   location = StringField('Location', validators=[Length(0, 64)])
   about_me = TextAreaField('About me')
   submit = SubmitField('Submit')

   def validate_email(self, field):
       if field.data != self.user.email and  User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
   def __init__(self, user, *args, **kwargs):
       super(EditProfileAdminForm, self).__init__(*args, **kwargs)
       self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
       self.user = user
       return
   def validate_username(self, field):
        if field.data != self.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')