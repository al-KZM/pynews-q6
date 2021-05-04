#!/usr/bin/python3

##############################################
#
# __init__.py
# main
#
##############################################
import flask

from .. import db, login_manager, mail_manager
from .. import mail_functions
from ..mixins import ModelMixin

main_blueprint = flask.Blueprint("main", __name__)

from . import routes, filters, models

