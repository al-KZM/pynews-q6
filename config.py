import os

basedir = os.path.abspath(os.path.dirname(__file__))


# https://flask.palletsprojects.com/en/1.1.x/config/
class Config:

    DEBUG = True
    SECRET_KEY = "my-very-secret-key"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    BASEDIR = basedir


    # MAIL CONFIG

    # pip install flask-mail
    MAIL_SERVER  = "smtp.gmail.com" # mail.yahoo.fr
    MAIL_PORT    = 587 # 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME       = 'elmozarello@gmail.com'
    MAIL_DEFAULT_SENDER = 'elmozarello@gmail.com'

    # Use an env variable:
    # In your terminal:
    # OSX: $ export MAIL_PASSWORD='mypassword' (To make it permanent, put this line in ~/.bash_profile)
    # WIN: Use cmder

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')






class PostgresConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/pynews"



configs = {
    "basic": Config,
    "postgres": PostgresConfig,
}

current_config = configs["basic"] # Replace with input ?


