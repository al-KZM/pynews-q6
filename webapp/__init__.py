import flask
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)

# In case you have: "A secret key is required to use..."
app.config["SECRET_KEY"] = "my-very-secret-key"

# Format of a postgresSQL database url:
# postgresql://<username>:<password>@<hostname>:<port>/<db_name>

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/pynews"

# WORKAROUND FOR DB ISSUES:
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = flask_sqlalchemy.SQLAlchemy(app)    # database bridge
migrate = flask_migrate.Migrate(app, db) # Migrator

from . import routes, models

