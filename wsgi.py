from webapp import create_app
from . import config

app = create_app(config.Config)
app.run(port=5000, debug=True)
