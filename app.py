from flask import Flask, render_template, redirect, url_for, flash

# Create a Flask application object.
app = Flask(__name__)
# Define app secret key.
app.secret_key = "keep this secret"
