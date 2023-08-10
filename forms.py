from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, SelectField
from wtforms.validators import NumberRange, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from lists import src_list


class CalculationForm(FlaskForm):
    file = FileField("Text file: ", validators=[FileRequired(), FileAllowed(
        ['txt'], "Please upload file in .txt format!")])
    src_name = SelectField("Source name: ", coerce=int,
                           choices=src_list, validators=[InputRequired()])
    diameter = DecimalField("Diameter of aperture (m): ", validators=[
                            InputRequired(), NumberRange(min=0)])
    submit = SubmitField("Compute")
