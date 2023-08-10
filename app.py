from flask import Flask, render_template, redirect, url_for, flash
from forms import CalculationForm
from lists import coeff_dict

# Create a Flask application object.
app = Flask(__name__)
# Define app secret key.
app.secret_key = "keep this secret"

# make a page that returns page not found


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


@app.route("/", methods=["GET", "POST"])
def home():
    '''Render homepage for calculations.'''
    cal_form = CalculationForm()
    if cal_form.validate_on_submit():
        pass
    return render_template("calculation.html", cal_form=cal_form, coeff_dict=coeff_dict)


if __name__ == "__main__":
    app.run(debug=True)
