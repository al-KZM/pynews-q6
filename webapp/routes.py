import flask

from . import app       # . is webapp/
from . import forms

@app.route("/")
def home():
    return "Hello world !"

@app.route('/test-form', methods=["GET", "POST"])
def test():
    # Create an instance of the form
    form = forms.TestForm()

    return flask.render_template("test_form.html", form=form)
