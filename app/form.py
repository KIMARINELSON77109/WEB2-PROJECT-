from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileAllowed, FileRequired, FileField


class ProfileForm(FlaskForm):
    FirstName = StringField('FirstName', validators=[InputRequired()])
    LastName = StringField('LastName', validators=[InputRequired()])
    gender = SelectField(label='Gender', choices=[("Female", "Female"), ("Male", "Male")])
    Email = StringField('Email', validators=[InputRequired(), Email()])
    Location = StringField('Location', validators=[InputRequired()])
    Biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('profile image', validators=[FileRequired(), FileAllowed(['jpg','png','jpeg'], 'Only image files are accepted with extensions "jpg","png","jpeg".')])
    button = SubmitField('Add Profile')
