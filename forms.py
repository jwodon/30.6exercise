from flask_wtf import FlaskForm
from wtforms import StringField, URLField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired, URL, AnyOf, NumberRange, Optional

class RegisterUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[Optional()])
    first_name = StringField("First Name", validators=[Optional()])
    last_name = StringField("Last Name", validators=[Optional()])

class LoginForm(FlaskForm):
    """Form for loggin in."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for feedback."""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])







