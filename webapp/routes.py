import flask, flask_login

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

@app.route("/sign-in", methods=["GET", "POST"])
def signin():
    form = forms.SignInForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Retrieve the user that matches this username
            user = models.User.query.filter_by(name=username).first()

            # Check the provided password against the user's one
            if user is not None and user.password == password:
                flask_login.login_user(user)
                flask.flash("User logged in successfully !", "success")
            else:
                flask.flash("Something went wrong.", "danger") # Put the message into the flashed messages
                # To retrieve those messages: flask.get_flashed_messages()

    return flask.render_template("signin.html", form=form)

@app.route("/sign-out")
def signout():
    flask_login.logout_user()
    return flask.redirect('/')


# Create a route that displays a list of all the registered users
@app.route("/users")
def users_list():
    # Retrieve users
    users = models.User.query.all()            # Return a list of users
    # users = [<User 1>, <User 2>]
    # my_user = users[0]
    # print(my_user.name)
    # print(my_user.password)


    # Create users_list.html
    return flask.render_template("users_list.html", users=users)


# Route: profile page
@app.route('/user/<int:user_id>')
def profile_page(user_id):

    # Query methods:
    # Class.query.all() --> Returns a list of all the objects
    # Class.query.filter_by(attr=value) --> Return a list of all the objects that match the condition
    # Class.query.get(primary_key) --> Retrieve an object by its PK

    # Retrieve the user
    user = models.User.query.get(user_id)

    return flask.render_template("user_profile.html", user=user)


@app.route('/quotes')
def quotes_list():
    # Retrieve the quotes
    quotes = models.Quote.query.all()

    # display them on a temlate
    return flask.render_template("quotes.html", quotes=quotes)

@app.route("/books")
def books_list():
    books = models.Book.query.all()

    return flask.render_template("books.html", books=books)

# Step 1: Displaying the favourite quote on the user page
# Step 2: (Because quote<->user is a one to one, one quote can be linked to only one user)
#       --> In quotes_list, display only the quotes that aren't the fav quote of a user
# Step 3: Creating a route fav_quote(quote_id) --> Sets the quote as the fav quote of the logged in
#        user
# Step 4: In the quotes_list: Add a button next to each quote (if the user is authenticated) to make
#        the quote his fav quote

@app.route("/fav-quote/<int:quote_id>")
def fav_quote(quote_id):
    if flask_login.current_user.is_authenticated: # The user is logged in
        # Retrieve the quote
        quote = models.Quote.query.get(quote_id)

        # Set this quote as the current user's fav one
        flask_login.current_user.fav_quote = quote

        # Commit our changes
        db.session.commit()

    return flask.redirect("/quotes")


@app.route("/fav_book/<int:book_id>")
def fav_book(book_id):
    if flask_login.current_user.is_authenticated: # The user is logged in
        book = models.Book.query.get(book_id) #book is an object of class Book

        flask_login.current_user.fav_books.append(book) # fav_books is a list of <Book> objects

        db.session.commit()

    return flask.redirect("/books")


@app.route("/populate")
def populate():
    return "Protected"
    import requests
    url = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json"
    books = requests.get(url).json()

    for book in books:
        try:
            book_obj = models.Book(title=book["title"])
            db.session.add(book_obj)
        except:
            pass

    db.session.commit()

    return "OK"










