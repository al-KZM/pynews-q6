import flask_wtf
import wtforms

# Form class --> flask_wtf.FlaskForm
# Form fields --> wtforms.SomethingField

# each form is a class inheriting from flask_wtf.FlaskForm
# every class attribute is a field in the form

# For example:
# A form with two fields:
#   - A name
#   - An age
class TestForm(flask_wtf.FlaskForm):

    name = wtforms.StringField("Name: ")
    age  = wtforms.IntegerField("Age: ")

    submit = wtforms.SubmitField("Submit the form !")

