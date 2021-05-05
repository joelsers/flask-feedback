from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class UserForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    email = StringField("email", validators = [InputRequired(),Email()])
    password = PasswordField("Password", validators = [InputRequired()])
    first_name = StringField("First name", validators = [InputRequired()])
    last_name = StringField("Last name", validators = [InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators = [InputRequired()])
    content = StringField("Content", validators = [InputRequired()])


class EditFeedback(FlaskForm):
    title = StringField("Title", validators = [InputRequired()])
    content = StringField("Content", validators = [InputRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])