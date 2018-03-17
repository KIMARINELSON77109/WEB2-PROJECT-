from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed, FileRequired, FileField
from app import allowed_extensions

class ProfileForm(FlaskForm):
    FirstName = StringField('First Name', validators = [DataRequired()])
    LastName = StringField('Last Name', validators = [DataRequired()])
    gender = SelectField(label='Select Gender', choices = [("None", "Select Gender"),("Female", "Female"), ("Male", "Male")])
    Email = StringField('Email', validators = [DataRequired(), Email()])
    Location = StringField('Location', validators = [DataRequired()])
    Biography = TextAreaField('Biography', validators = [DataRequired()])
    photo = FileField(validators=[FileRequired(), FileAllowed(allowed_extensions)])