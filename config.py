

basedir = os.path.abspath(os.path.dirname(__file__))


# https://flask.palletsprojects.com/en/1.1.x/config/
class Config:

    DEBUG = True
    SECRET_KEY = "my-very-secret-key"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    BASEDIR = basedir


class PostgresConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/pynews"

configs = {
    "basic": Config,
    "postgres": PostgresConfig,
}
