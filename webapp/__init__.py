import flask
import flask_login, flask_mail, flask_sqlalchemy, flask_migrate, flask_babel


import os


# Init all the managers variables
db = flask_sqlalchemy.SQLAlchemy()              # database bridge
migrate = flask_migrate.Migrate()               # Migrator
login_manager = flask_login.LoginManager()
mail_manager = flask_mail.Mail()
babel        = flask_babel.Babel()


def create_app(conf):
    from .auth import auth_blueprint
    from .main import main_blueprint

    app = flask.Flask(__name__)

    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(db=db, app=app)
    login_manager.init_app(app)
    mail_manager.init_app(app)
    babel.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


@babel.localeselector
def get_locale():
    lang = flask.session.get("language")
    if lang is not None:
        return lang

    # if a user is logged in, use the locale from the user settings
    user = getattr(flask.g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return flask.request.accept_languages.best_match(['he', 'sp', 'fr', 'en'])

