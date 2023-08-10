from flask import Flask, render_template, redirect, url_for, flash, request
from forms import CalculationForm
from lists import coeff_dict, src_list
import math

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
    return render_template("calculation.html", cal_form=cal_form, coeff_dict=coeff_dict)


@app.route("/result", methods=["POST"])
def result():
    cal_form = CalculationForm()
    if cal_form.validate_on_submit():
        src_idx = cal_form.src_name.data
        src = src_list[src_idx][1]
        diameter = cal_form.diameter.data
        obs_freq = 1.395
        s_v = coeff_dict[src]["a0"]
        t_a = 1
        eta_a = 1
        a_eff = eta_a * math.pi / 4 * (float(diameter)**2)
        print("successful")
        flash("Calculation successful!", "success")
        return render_template("result.html", coeff_dict=coeff_dict, src=src, diameter=diameter, obs_freq=obs_freq, s_v=s_v, t_a=t_a, eta_a=eta_a, a_eff=a_eff)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
