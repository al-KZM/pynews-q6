import flask

from . import app, db       # . is webapp/
from . import forms, news_functions, models

@app.route("/")
def home():
    return "Hello world !"

## Create a route:
# Form with one single field "query"
# Use the form data to display some articles about the query

# 1) Create the form        v
# 2) Create the route
# 3) Create the template that displays the form
# 4) Create the template that displays the articles

@app.route("/article/query/<query>")
def query_article(query):
    articles = news_functions.get_news(query)
    return flask.render_template("articles.html", articles=articles)

@app.route("/search-article", methods=["GET", "POST"])
def search_article():
    form = forms.QueryForm()

    # case 1: Post request --> The user is sending data
    if flask.request.method == "POST":
        if form.validate_on_submit(): # Check all the validators
            url = flask.url_for("query_article", query=form.query.data)
            # url --> /article/query/rick
            return flask.redirect(url)


    # case 2: Get request --> the user just wants to see the page
    return flask.render_template("search_article.html", form=form)

# Sign up page

# Create a page that displays a sign up form (username & password) and when it gets data from a user
# just print "Rick is signing up with password chocolate"

# The password needs to contain 6 to 12 characters
@app.route("/sign-up", methods=["GET","POST"])
def signup():
    """
    The function needs to add the user to the DB
    :return:
    """
    form = forms.SignUpForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Create user
            user = models.User(name=username, password=password)
            # Add it to the DB
            db.session.add(user)
            # Commit your changes
            db.session.commit()
            print(f"{username} was registered successfully")

    return flask.render_template("signup.html", form=form)


# Create a route that displays a list of all the registered users
@app.route("/users")
def users_list():
    # Retrieve users
    users = models.User.query.all()            # Return a list of users
    # Create users_list.html
    return flask.render_template("users_list.html", users=users)
















