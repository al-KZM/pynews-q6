import flask

app = flask.Flask(__name__)

# In case you have: "A secret key is required to use..."
app.config["SECRET_KEY"] = "my-very-secret-key"

from . import routes

