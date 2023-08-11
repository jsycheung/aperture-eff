from flask import Flask, render_template, redirect, url_for, flash, request
from forms import CalculationForm
from lists import coeff_dict, src_list
from calc_values import calc_Ta_obs
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
        file = request.files['file']
        t_a_prime, t_a_std, obs_freq = calc_Ta_obs(file)
        src_idx = cal_form.src_name.data
        src = src_list[src_idx][1]
        diameter = cal_form.diameter.data
        s_v = coeff_dict[src]["a0"] + coeff_dict[src]["a1"]*math.log10(obs_freq) + coeff_dict[src]["a2"]*(math.log10(obs_freq))**2 + coeff_dict[src]["a3"]*(
            math.log10(obs_freq))**3 + coeff_dict[src]["a4"]*(math.log10(obs_freq))**4 + coeff_dict[src]["a5"]*(math.log10(obs_freq))**5
        eta_a = 3520/(float(diameter)**2)*t_a_prime/s_v
        a_eff = eta_a * math.pi / 4 * (float(diameter)**2)
        flash("Calculation successful!", "success")
        return render_template("result.html", coeff_dict=coeff_dict, src=src, diameter=diameter, obs_freq=obs_freq, s_v=s_v, t_a_prime=t_a_prime, t_a_std=t_a_std, eta_a=eta_a, a_eff=a_eff)
    print(cal_form.errors)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
