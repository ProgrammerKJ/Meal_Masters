from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
from bs4 import BeautifulSoup
from config import SPOONACULAR_API_KEY

from models import User, Recipe, db, connect_db, SavedRecipe, WeightEntry
from forms import UserSignupForm, UserLoginForm, UserEditForm, RecipeSearchForm, WeightEntryForm

CURR_USER_KEY = "curr_user"
base_url = 'https://api.spoonacular.com/recipes/complexSearch'


app = Flask(__name__)
app.debug = True


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lukadon1996$@localhost/fitness_app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kfvmfvmz:4mUqTDX3PjemP58zn7Z-DgHy6_7kRHjU@kala.db.elephantsql.com/kfvmfvmz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"

toolbar = DebugToolbarExtension(app)


with app.app_context():
    connect_db(app)
    db.create_all()


# Basic Logout, Login, Add user to g functionality

@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):

    session[CURR_USER_KEY] = user.user_id


def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# Login, Signup & Logout Routes

@app.route('/signup', methods=["GET", "POST"])
def signup():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserSignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()

        except IntegrityError as e:
            flash("This username is unavailable, please select another one", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect(f'/users/{user.user_id}')

    else:

        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect(f'/users/{user.user_id}')
        else:
            flash("Wrong username or password", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():

    do_logout()

    flash("You have been successfully logged out", 'success')
    return redirect("/login")


# View, Edit, Delete User
def fetch_random_fitness_quote():
    category = 'fitness'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(
        category)

    try:
        response = requests.get(
            api_url, headers={'X-Api-Key': 'LfaJEUA3LNJavnw+MZIvxw==OG0QYXLeAfiMZ4sT'})
        if response.status_code == requests.codes.ok:
            quote = response.json()
            return quote
        else:
            return None
    except Exception as e:
        return None


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def users_profile(user_id):
    user = User.query.get_or_404(user_id)

    quote = fetch_random_fitness_quote()

    return render_template('users/profile.html', user=user, quote=quote)


@app.route('/weight_entry', methods=['GET', 'POST'])
def weight_entry():

    if not g.user:
        flash("Access Denied.", "danger")
        return redirect('/')

    user = g.user

    form = WeightEntryForm()

    if form.validate_on_submit():
        date = form.date.data
        weight = form.weight.data
        goal_weight = form.goal_weight.data

        entry = WeightEntry(user_id=user.user_id, date=date,
                            weight=weight, goal_weight=goal_weight)
        db.session.add(entry)
        db.session.commit()

        flash('Weight entry added successfully!', 'success')
        return redirect(url_for('weight_tracker'))

    return render_template('users/weight_entry.html', form=form)


@app.route('/weight_tracker', methods=['GET'])
def weight_tracker():

    if not g.user:
        flash("Access Denied.", "danger")
        return redirect('/')

    user = g.user

    weight_entries = WeightEntry.query.filter_by(
        user_id=user.user_id).order_by(WeightEntry.date.desc()).all()

    return render_template('users/weight_tracker.html', weight_entries=weight_entries)


@app.route('/users/edit', methods=["GET", "POST"])
def edit_profile():

    if not g.user:
        flash("Access Denied.", "danger")
        return redirect('/')

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default_user_icon.png"

            db.session.commit()
            return redirect(f"/users/{user.user_id}")
        else:
            flash("Sorry! Wrong password, try again", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.user_id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


def calculate_total_pages(total_results, number_per_page):
    return (total_results + number_per_page - 1) // number_per_page


@app.route('/search_recipe', methods=['GET'])
def search_recipe():

    page = request.args.get('page', default=1, type=int)
    number_per_page = 20

    form = RecipeSearchForm()

    if 'page' in request.args:
        next_page = page + 1
        total_results = int(request.args.get('total_results', 0))
        total_pages = calculate_total_pages(total_results, number_per_page)

        if next_page <= total_pages:
            return redirect(url_for('search_results', page=next_page, total_results=total_results))

    total_results = 0

    return render_template('recipes/search_recipes.html', form=form, total_results=total_results)


@app.route('/search_results', methods=['GET'])
def search_results():
    page = request.args.get('page', default=1, type=int)
    total_results = int(request.args.get('total_results', 0))
    number_per_page = 20

    params = {
        'query': request.args.get('query', ''),
        'cuisine': request.args.get('cuisine', ''),
        'diet': request.args.get('diet', ''),
        'apiKey': SPOONACULAR_API_KEY,
        'number': number_per_page,
        'offset': (page - 1) * number_per_page,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        recipes = data.get('results', [])
        total_results = data.get('totalResults', 0)

        total_pages = calculate_total_pages(total_results, number_per_page)

    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=str(e))

    return render_template('recipes/search_results.html', recipes=recipes, page=page, total_pages=total_pages, total_results=total_results)


@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    base_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'includeNutrition': True,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        recipe_details = response.json()

        ingredients_data = recipe_details.get('extendedIngredients', [])
        ingredients = [ingredient.get('original', '')
                       for ingredient in ingredients_data]

        instructions_html = recipe_details.get('instructions', '')
        soup = BeautifulSoup(instructions_html, 'html.parser')
        instructions_text = soup.get_text(separator='. ')

        instructions = instructions_text.split('. ')

        nutrition_data = recipe_details.get(
            'nutrition', {}).get('nutrients', [])
        nutrients_to_display = [
            'Calories',
            'Fat',
            'Saturated Fat',
            'Carbohydrates',
            'Net Carbohydrates',
            'Sugar',
            'Cholesterol',
            'Sodium',
            'Protein',
        ]
        filtered_nutrition = [
            nutrient for nutrient in nutrition_data if nutrient['name'] in nutrients_to_display
        ]

        add_to_saved_recipes = True

        if request.method == 'POST':
            user = g.user
            recipe = Recipe.query.get_or_404(recipe_id)

            if recipe not in user.saved_recipes:

                user.saved_recipes.append(recipe)
                db.session.commit()
                flash("Recipe saved successfully!", "success")
                add_to_saved_recipes = False
            else:
                flash("Recipe already saved.", "warning")

        return render_template('recipes/view_recipe.html', recipe_details=recipe_details, ingredients=ingredients, instructions=instructions, total_nutrition=filtered_nutrition, add_to_saved_recipes=add_to_saved_recipes, recipe_id=recipe_id)

    except requests.exceptions.RequestException as e:

        return render_template('error.html', error_message=str(e))


@app.route('/save_recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):

    if not g.user:
        flash("Access Denied. Please log in or sign up.", "danger")
        return redirect('/login')

    user = g.user

    recipe_id = request.form.get('recipe_id', type=int)

    if not SavedRecipe.query.filter_by(user_id=user.user_id, recipe_id=recipe_id).first():
        saved_recipe = SavedRecipe(user_id=user.user_id, recipe_id=recipe_id)
        db.session.add(saved_recipe)
        db.session.commit()
        flash("Recipe saved successfully!", "success")
    else:
        flash("Recipe already saved.", "warning")

    return redirect(url_for('view_recipe', recipe_id=recipe_id))


def fetch_recipe_details(recipe_id):
    base_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'includeNutrition': True,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        recipe_details = response.json()
        return recipe_details
    except requests.exceptions.RequestException as e:
        return None


@app.route('/saved_recipes')
def saved_recipes():

    if not g.user:
        flash("Access Denied. Please log in or sign up.", "danger")
        return redirect('/login')

    user = g.user

    saved_recipe_ids = [saved.recipe_id for saved in user.saved_recipe_ids]

    saved_recipes = []

    desired_nutrient_names = [
        "Calories",
        "Fat",
        "Saturated Fat",
        "Carbohydrates",
        "Net Carbohydrates",
        "Sugar",
        "Cholesterol",
        "Sodium",
        "Protein",
    ]

    for recipe_id in saved_recipe_ids:

        recipe_details = fetch_recipe_details(recipe_id)

        if recipe_details:
            fetched_recipe_title = recipe_details.get('title', '')
            fetched_recipe_image = recipe_details.get('image', '')
            fetched_recipe_ingredients = recipe_details.get(
                'extendedIngredients', [])

            fetched_recipe_instructions = recipe_details.get(
                'instructions', '')

            fetched_recipe_nutrition = recipe_details.get(
                'nutrition', {}).get('nutrients', [])

            filtered_nutrition = [nutrient for nutrient in fetched_recipe_nutrition if nutrient.get(
                'name') in desired_nutrient_names]

            unique_ingredients = set()

            for ingredient in fetched_recipe_ingredients:
                original_ingredient = ingredient.get('original')
                if original_ingredient:
                    unique_ingredients.add(original_ingredient)

            instructions_html = fetched_recipe_instructions
            instructions_text = BeautifulSoup(
                instructions_html, 'html.parser').get_text()

            instructions_steps = [step.strip()
                                  for step in instructions_text.split('.')]

            instructions_steps = [step for step in instructions_steps if step]

            saved_recipe_data = {
                'id': recipe_id,
                'title': fetched_recipe_title,
                'image': fetched_recipe_image,
                'unique_ingredients': unique_ingredients,
                'unique_instructions': '\n'.join(instructions_steps),
                'nutrition': filtered_nutrition
            }

            saved_recipes.append(saved_recipe_data)

    return render_template('recipes/saved_recipes.html', saved_recipes=saved_recipes)


@app.route('/remove_saved_recipe/<int:recipe_id>', methods=['POST'])
def remove_saved_recipe(recipe_id):
    if not g.user:
        flash("Access Denied. Please log in or sign up.", "danger")
        return redirect('/login')

    user = g.user

    saved_recipe = SavedRecipe.query.filter_by(
        user_id=user.user_id, recipe_id=recipe_id).first()

    if saved_recipe:
        db.session.delete(saved_recipe)
        db.session.commit()
        flash("Recipe removed from saved recipes.", "info")

    return redirect('/saved_recipes')


@app.route('/shoppinglist')
def shopping_list():
    return render_template('users/shopping_list.html')


@app.route('/')
def index():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
