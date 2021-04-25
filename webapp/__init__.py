import flask
import flask_sqlalchemy
import flask_migrate
import flask_login

import os


basedir = os.path.abspath(os.path.dirname(__file__))


db = flask_sqlalchemy.SQLAlchemy()              # database bridge
migrate = flask_migrate.Migrate()               # Migrator
login_manager = flask_login.LoginManager()


def create_app():

    app = flask.Flask(__name__)

    from .auth import auth_blueprint
    from . import routes, models, filters

    app.config["SECRET_KEY"] = "my-very-secret-key"

    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/pynews"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')


    db.init_app(app)
    migrate.init_app(db=db, app=app)
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


