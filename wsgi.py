from webapp import create_app


app = create_app()

app.run(port=5000, debug=True)
