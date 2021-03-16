from . import app       # . is webapp/

@app.route("/")
def home():
    return "Hello world !"