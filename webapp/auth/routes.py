import flask, flask_login

from . import auth_blueprint, db
from . import forms, models

# The password needs to contain 6 to 12 characters
@auth_blueprint.route("/sign-up", methods=["GET","POST"])
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
            mail     = form.mail.data

            # Create user
            user = models.User(name=username, mail=mail)

            user.set_password(password)

            # Add it to the DB
            db.session.add(user)
            # Commit your changes
            db.session.commit()
            print(f"{username} was registered successfully")

    return flask.render_template("signup.html", form=form)

@auth_blueprint.route("/sign-in", methods=["GET", "POST"])
def signin():
    form = forms.SignInForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Retrieve the user that matches this username
            user = models.User.query.filter_by(name=username).first()

            # Check the provided password against the user's one
            if user is not None and user.check_password(password):
                flask_login.login_user(user)
                flask.flash("User logged in successfully !", "success")
            else:
                flask.flash("Something went wrong.", "danger") # Put the message into the flashed messages
                # To retrieve those messages: flask.get_flashed_messages()

    return flask.render_template("signin.html", form=form)

@auth_blueprint.route("/sign-out")
def signout():
    flask_login.logout_user()
    return flask.redirect('/')

@auth_blueprint.route("/reset-password/<int:user_id>")
def reset_password(user_id):
    form = forms.ResetPasswordForm()

    user = models.User.get(user_id)

    if not user:
        flask.flash("User doesn't exist")
        return flask.redirect('/')

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user.set_password(form.password.data)

            flask.flash("Password has been reset successfully")

            return flask.redirect('/')

    return flask.render_template("reset_password.html")


@auth_blueprint.route("/forgot-password")
def forgot_password():

    form = forms.ForgotPasswordform()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            # Fetch the user with this username
            user = models.User.query.filter_by(name=username).first()
            if user:
                # User is not none

                # Without _external=True:
                # /reset-password/8
                # With _external=True:
                # www.pynews.com/reset-password/8
                reset_link = flask.url_for('reset_password', user_id=user.id, _external=True)
                mail_functions.send_mail(
                    title="Password Reset",
                    body=f"Hey, to reset your email, follow this link: {reset_link}",
                    recipients=user.mail,
                )

                flask.flash("A reset link has been sent to your mail.")


            else:
                flask.flash(f"User {username} doesn't exist")


    return flask.render_template("")
