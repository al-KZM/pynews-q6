from webapp import create_app
import config


app = create_app(config.current_config)
app.run(port=5000, debug=True)
