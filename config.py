import os

basedir = os.path.abspath(os.path.dirname(__file__))


# https://flask.palletsprojects.com/en/1.1.x/config/
class Config:

    BASEDIR = basedir
    UPLOADS_DIR = os.path.join(basedir, 'webapp/uploads')


class DevConfig(Config):
    """
    Development config
    """

    DEBUG = True
    SECRET_KEY = "my-very-secret-key"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


    MAIL_SERVER  = "smtp.gmail.com" # mail.yahoo.fr
    MAIL_PORT    = 587 # 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME       = 'elmozarello@gmail.com'
    MAIL_DEFAULT_SENDER = 'elmozarello@gmail.com'

    # Somewhere you need to do (probably in ~/.bash_profile):
    # export MAIL_PASSWORD="mypassword"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class ProdConfig(Config):
    """
    Production config
    """
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    MAIL_SERVER  = "smtp.gmail.com" # mail.yahoo.fr
    MAIL_PORT    = 587 # 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME       = 'elmozarello@gmail.com'
    MAIL_DEFAULT_SENDER = 'elmozarello@gmail.com'

    # Somewhere you need to do (probably in ~/.bash_profile):
    # export MAIL_PASSWORD="mypassword"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



configs = {
    "dev": DevConfig,
    "prod": ProdConfig,
}

if os.environ.get("FLASK_ENV") == "dev":
    current_config = configs["dev"] # Replace with input ?
else:
    current_config = configs["prod"] # Replace with input ?




