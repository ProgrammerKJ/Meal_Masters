from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image_url = db.Column(
        db.Text, default="/static/images/default_user_icon.png")

    current_weight = db.Column(db.Float, nullable=True)
    goal_weight = db.Column(db.Float, nullable=True)
    current_body_fat = db.Column(db.Float, nullable=True)
    goal_body_fat = db.Column(db.Float, nullable=True)

    saved_recipe_ids = db.relationship(
        'SavedRecipe', back_populates='user', cascade='all, delete-orphan'
    )

    @classmethod
    def signup(cls, username, email, password, image_url=None):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url or User.image_url.default.arg,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user


class SavedRecipe(db.Model):
    __tablename__ = 'saved_recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'))
    recipe_id = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='saved_recipe_ids')


class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    goal_weight = db.Column(db.Float)


class Recipe(db.Model):

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)


def connect_db(app):

    db.app = app
    db.init_app(app)
