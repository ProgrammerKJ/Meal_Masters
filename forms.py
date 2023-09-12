from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField, BooleanField, SelectField, SubmitField, DecimalField, FloatField, DateField
from wtforms.validators import DataRequired, Email, Length


class UserSignupForm(FlaskForm):
    """Adding users to database"""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField(
        'E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Profile Avatar')


class UserEditForm(FlaskForm):
    """Edit user profile"""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField(
        'E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Profile Avatar')
    password = PasswordField('Password', validators=[Length(min=6)])


class UserLoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class RecipeSearchForm(FlaskForm):
    query = StringField('Search Query')
    cuisine = StringField('Cuisine')
    diet = SelectField('Diet', choices=[('', 'Select Diet (Optional)'), ('vegetarian', 'Vegetarian'), (
        'vegan', 'Vegan'), ('gluten free', 'Gluten Free')])
    include_nutrition = BooleanField('Include Nutrition')
    submit = SubmitField('Search')


class WeightEntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    weight = FloatField('Weight (lbs)', validators=[DataRequired()])
    goal_weight = FloatField('Goal Weight (lbs)')
    submit = SubmitField('Submit')
