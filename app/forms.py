from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import images

class UploadForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    image = FileField('Drawing Image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])
    submit = SubmitField('Analyse')