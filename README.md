# Meal Masters - Your Recipe and Diet Tracking App

Meal Masters is a web-based application that empowers users to discover, plan, and track their culinary journey. Whether you're a seasoned chef or a cooking novice, Meal Masters has something for you. With Meal Masters, you can:

- **Search for Recipes**: Explore a vast collection of recipes using the Spoonacular API. Find recipes that match your dietary preferences, cuisine choices, or ingredients on hand.

- **Plan Your Meals**: Create a personalized meal plan by adding your favorite recipes. Whether it's breakfast, lunch, dinner, or snacks, Meal Masters helps you organize your culinary adventures.

- **Track Your Progress**: Keep an eye on your health and fitness goals. Log your current weight and set a target weight to monitor your dieting progress over time.

- **Create a Shopping List**: Never forget an ingredient again! With Meal Masters' built-in shopping list, you can easily compile the ingredients you need for your meal plan.

## Technologies Used

Meal Masters is built with a variety of technologies to provide a seamless and user-friendly experience:

- **Backend**: Python and Flask are used to create a robust backend server that handles user authentication, data storage, and API interactions.

- **Frontend**: HTML, CSS, and JavaScript form the foundation of the user interface, providing an intuitive and responsive design.

- **Database**: PostgreSQL is the chosen database management system to store user data, recipes, and weight tracking information.

## Getting Started

To get started with Meal Masters, follow these steps:

1. **Clone the Repository**: Clone this GitHub repository to your local machine using the following command:

   ```shell
   git clone https://github.com/Nepalimolly/Meal_Masters.git
   ```

2. **Set Up a Python Virtual Environment**: Create a virtual environment to manage Python dependencies. You can use `venv` or `virtualenv` for this purpose.

3. **Install Dependencies**: Install the required Python packages using pip. You can find the list of dependencies in the `requirements.txt` file.

4. **Set Up Your Database**: Meal Masters uses PostgreSQL as the database. Create a PostgreSQL database and update the database URI in your Flask configuration.

5. **Run the Application**: Start the Flask application. You can typically do this with the following command:

   ```shell
   flask run
   ```

6. **Access the Application**: Open your web browser and navigate to `http://127.0.0.1:5000` to access Meal Masters locally.
7. **Test the Application**: Test the application. You can typically do this with the following command:
   ```shell
   pytest -v
   ```

## Usage

- **User Authentication**: Sign up for a new account, log in with your credentials, and log out when you're done.

- **Recipe Search**: Use the powerful Spoonacular API to search for recipes based on your preferences. Filter by cuisine, dietary restrictions, and more.

- **Meal Planning**: Create your meal plan by adding recipes to your schedule. Plan your breakfast, lunch, dinner, and snacks effortlessly.

- **Weight Tracking**: Log your current weight and set a target weight to track your progress over time.

- **Shopping List**: Add ingredients from your meal plan to your shopping list. Take it with you when you go grocery shopping.

---
