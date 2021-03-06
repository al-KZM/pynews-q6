import flask, flask_login
import jwt      # Not pyjwt, altough it's the name of the package you need to install

from . import auth_blueprint, db
from . import forms, models, mail_functions

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

            #profile_pic = form.profile_pic.data
            #filepath = "/uploads/pic1"
            #profile_pic.save(filepath)


            # Create user
            user = models.User(name=username, mail=mail)

            user.set_password(password)

            user.save()

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

    return flask.render_template("signin.html", signin_form=form)

@auth_blueprint.route("/sign-out")
def signout():
    flask_login.logout_user()
    return flask.redirect('/')

@auth_blueprint.route("/reset-password/<token>", methods=["GET","POST"])
def reset_password(token):
    form = forms.ResetPasswordForm()

    try:
        payload = jwt.decode(token, flask.current_app.config["SECRET_KEY"], algorithms=['HS256'])
        user_id = payload["user_id"]
        user = models.User.query.get(user_id)
    except Exception as e:
        print(str(e))
        flask.flash("Something went wrong.")
        return flask.redirect('/')

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user.set_password(form.password.data)

            flask.flash("Password has been reset successfully")

            return flask.redirect('/')

    return flask.render_template("reset_password.html", form=form)


@auth_blueprint.route("/forgot-password", methods=["GET","POST"])
def forgot_password():

    form = forms.ForgotPasswordform()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            # Fetch the user with this username
            user = models.User.query.filter_by(name=username).first()
            if user:
                # User is not none

                # Generate an encrypted token
                payload = {
                    "user_id": user.id,
                }
                token = jwt.encode(payload, flask.current_app.config["SECRET_KEY"], algorithm="HS256")

                # Without _external=True:
                # /reset-password/8
                # With _external=True:
                # 127.0.0.1:5000/reset-password/8 (or www.pynews.com/reset-password/8)
                reset_link = flask.url_for('auth.reset_password', token=token, _external=True)
                mail_functions.send_mail(
                    title="Password Reset",
                    body=f"Hey, to reset your email, follow this link: {reset_link}",
                    recipients=user.mail,
                )

                flask.flash("A reset link has been sent to your mail.")


            else:
                flask.flash(f"User {username} doesn't exist")


    return flask.render_template("forgot_password.html", form=form)
