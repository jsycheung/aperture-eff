from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField
from wtforms.validators import NumberRange


class CalculationForm(FlaskForm):
    obsfreq = DecimalField("Observation Frequency", validators=[
        NumberRange(min=0)])
    submit = SubmitField("Submit")
