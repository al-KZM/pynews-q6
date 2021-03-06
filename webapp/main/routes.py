import flask, flask_login

from . import main_blueprint, db       # . is webmain_blueprint/
from . import forms, news_functions, mail_functions, models


@main_blueprint.route("/test")
def test():
    flask.flash("Testing mail sending !")

    mail_functions.send_mail(title="Hello world",
                             body="This is a test !",
                             recipients="eyal@chocron.eu",
                             html=flask.render_template('mail.html', body="Hello World !")
                            )

    return flask.redirect('/')


@main_blueprint.route("/set-language/<lang>")
def set_language(lang):
    flask.session["language"] = lang
    flask_babel.refresh()
    return flask.redirect('/')

@main_blueprint.route("/")
def home():
    return "Hello world !"

## Create a route:
# Form with one single field "query"
# Use the form data to display some articles about the query

# 1) Create the form        v
# 2) Create the route
# 3) Create the template that displays the form
# 4) Create the template that displays the articles

@main_blueprint.route("/article/query/<query>")
def query_article(query):
    articles = news_functions.get_news(query)
    return flask.render_template("articles.html", articles=articles)

@main_blueprint.route("/search-article", methods=["GET", "POST"])
def search_article():
    form = forms.QueryForm()

    # case 1: Post request --> The user is sending data
    if flask.request.method == "POST":
        if form.validate_on_submit(): # Check all the validators
            url = flask.url_for("main.query_article", query=form.query.data)
            # url --> /article/query/rick
            return flask.redirect(url)


    # case 2: Get request --> the user just wants to see the page
    return flask.render_template("search_article.html", form=form)


# Create a route that displays a list of all the registered users
@main_blueprint.route("/users")
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
@main_blueprint.route('/user/<int:user_id>')
def profile_page(user_id):

    # Query methods:
    # Class.query.all() --> Returns a list of all the objects
    # Class.query.filter_by(attr=value) --> Return a list of all the objects that match the condition
    # Class.query.get(primary_key) --> Retrieve an object by its PK

    # Retrieve the user
    user = models.User.query.get(user_id)

    return flask.render_template("user_profile.html", user=user)


@main_blueprint.route('/quotes')
def quotes_list():
    # Retrieve the quotes
    quotes = models.Quote.query.all()

    # display them on a temlate
    return flask.render_template("quotes.html", quotes=quotes)

@main_blueprint.route("/books")
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

@main_blueprint.route("/fav-quote/<int:quote_id>")
def fav_quote(quote_id):
    if flask_login.current_user.is_authenticated: # The user is logged in
        # Retrieve the quote
        quote = models.Quote.query.get(quote_id)

        # Set this quote as the current user's fav one
        flask_login.current_user.fav_quote = quote

        # Commit our changes
        db.session.commit()

    return flask.redirect(flask.url_for('quotes_list'))


@main_blueprint.route("/fav_book/<int:book_id>")
def fav_book(book_id):
    """
    Add a book to the logged in user's favourite books

    :param book_id: (int) id of the book
    :return: A redirection to /books (or /sign-in if the user is anonymous)
    """
    # Check if user is authenticated
    if flask_login.current_user.is_authenticated:
        # Retrieving the book object from the database
        book = models.Book.query.get(book_id)

        # Adding it to the user's fav books if it's not already in
        if book not in flask_login.current_user.fav_books:
            flask_login.current_user.fav_books.append(book)
            db.session.commit()
    else:
        # User not logged in, flash an error message and redirect him to sign-in page
        flask.flash("You need to be logged in")
        return flask.redirect("/sign-in")

    return flask.redirect("/books")


@main_blueprint.route("/populate")
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










