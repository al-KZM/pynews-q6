import flask
from .. import db, login_manager
from .. import mail_functions

auth_blueprint = flask.Blueprint('auth', __name__)

from . import routes, models # Python needs to read those files !

