# Meal Masters 🍽️

**A comprehensive Flask-based meal planning and nutrition tracking application that empowers users to discover recipes, plan meals, and monitor their fitness journey.**

🎥 **Video Walkthrough:** [Watch Demo](https://www.loom.com/share/c4aa7d9e35c24ec5832cdf50c5bd368d?sid=40d42fe1-5764-459b-b8ec-549effb7375f)  

## ✨ Key Features

### 🔍 Recipe Discovery & Management
- **Advanced Recipe Search** powered by Spoonacular API with 380,000+ recipes
- **Smart Filtering** by cuisine, dietary restrictions (vegetarian, vegan, gluten-free)
- **Detailed Nutritional Information** with calorie tracking and macro breakdown
- **Personal Recipe Collection** with save/remove functionality
- **Shopping List Generation** from saved recipes and meal plans

### 📊 Health & Fitness Tracking
- **Weight Progress Monitoring** with goal setting and historical tracking
- **Visual Progress Charts** showing weight trends over time
- **Goal-Oriented Planning** with target weight functionality
- **Date-Based Entry System** for accurate progress tracking

### 👤 User Management & Security
- **Secure Authentication** with bcrypt password hashing
- **Session Management** with Flask sessions and CSRF protection
- **Profile Customization** with avatar upload and account editing
- **Protected Routes** ensuring data privacy and security

### 🎨 User Experience
- **Responsive Design** optimized for all devices
- **Intuitive Navigation** with clean, modern interface
- **Real-time Search Results** with pagination and filtering
- **Motivational Quotes** from fitness API integration

## 🛠️ Technical Stack

### **Backend (Python/Flask)**
- **Flask Framework** for robust web application architecture
- **SQLAlchemy ORM** for database abstraction and relationships
- **Flask-WTF** for form handling and CSRF protection
- **Flask-Bcrypt** for secure password hashing
- **PostgreSQL** for production-grade data persistence

### **External API Integration**
- **Spoonacular API** for comprehensive recipe and nutrition data
- **API-Ninjas** for motivational fitness quotes
- **BeautifulSoup** for HTML parsing and data extraction
- **Requests** library for HTTP API communication

### **Frontend Technologies**
- **Jinja2 Templating** for dynamic content rendering
- **HTML5/CSS3** with responsive design principles
- **JavaScript** for interactive user interface elements
- **Bootstrap** for consistent styling and layout

### **Testing & Quality Assurance**
- **Pytest** for comprehensive integration testing
- **Unittest** for model and route testing
- **Test Database** setup with proper isolation
- **95%+ test coverage** across all application layers

## 🏗️ Application Architecture

```
Flask Application
├── Models (SQLAlchemy)
│   ├── User (Authentication & Profiles)
│   ├── SavedRecipe (Recipe Collections)
│   └── WeightEntry (Fitness Tracking)
├── Views/Routes
│   ├── Authentication (Login/Signup/Logout)
│   ├── Recipe Management (Search/Save/View)
│   ├── Weight Tracking (Entry/Progress)
│   └── User Profile (Edit/Delete)
├── Forms (WTForms)
│   ├── User Forms (Signup/Login/Edit)
│   ├── Recipe Search Forms
│   └── Weight Entry Forms
└── External APIs
    ├── Spoonacular (Recipe Data)
    └── API-Ninjas (Fitness Quotes)
```

## 📊 Database Schema

**Core Models:**
```python
User:
├── user_id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password (Hashed)
├── image_url
└── saved_recipe_ids (Relationship)

SavedRecipe:
├── id (Primary Key)
├── user_id (Foreign Key)
├── recipe_id (Spoonacular ID)
└── user (Relationship)

WeightEntry:
├── id (Primary Key)
├── user_id (Foreign Key)
├── date
├── weight
└── goal_weight
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Spoonacular API Key ([Get Free Key](https://spoonacular.com/food-api))

### Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/programmerKJ/Meal_Masters.git
cd Meal_Masters
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration:**
Create `config.py` file:
```python
SPOONACULAR_API_KEY = "your_spoonacular_api_key"
SECRET_KEY = "your_secret_key"
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost/meal_masters"
```

5. **Database Setup:**
```bash
# Create PostgreSQL database
createdb meal_masters

# Initialize database tables
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

6. **Start the application:**
```bash
flask run
# Application runs on http://127.0.0.1:5000
```

## 🧪 Testing

### Run Test Suite
```bash
# Unit and Route Tests
python -m pytest test_models.py -v
python -m pytest test_routes.py -v

# Integration Tests
python -m pytest test_integration.py -v

# All Tests
pytest -v

# Test Coverage Report
pytest --cov=app --cov-report=html
```

### Test Categories
- **Model Testing:** User authentication, recipe saving, weight tracking
- **Route Testing:** All endpoints with proper status codes
- **Integration Testing:** End-to-end user workflows
- **API Testing:** External API integration and error handling

## 🎯 Technical Highlights

### Advanced Flask Patterns
```python
# Secure Authentication with Session Management
@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

# API Integration with Error Handling
def fetch_recipe_details(recipe_id):
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
```

### Database Relationship Management
```python
# One-to-Many Relationships with Cascade Delete
saved_recipe_ids = db.relationship(
    'SavedRecipe', 
    back_populates='user', 
    cascade='all, delete-orphan'
)
```

### Form Validation and Security
```python
# WTForms with Custom Validators
class UserSignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
```

## 📈 Performance & Security Features

- **Password Security:** bcrypt hashing with salt rounds
- **Session Management:** Secure cookie handling with CSRF protection
- **Database Optimization:** Efficient queries with SQLAlchemy relationships
- **API Rate Limiting:** Intelligent caching for external API calls
- **Input Validation:** Comprehensive form validation and sanitization
- **Error Handling:** Graceful degradation with user-friendly error messages

## 🔮 Future Enhancements

- [ ] **Social Features** - Share meal plans and recipes with friends
- [ ] **Meal Plan Calendar** - Weekly/monthly meal planning interface
- [ ] **Barcode Scanner** - Quick ingredient and nutrition lookup
- [ ] **Mobile App** - React Native companion application
- [ ] **Advanced Analytics** - Detailed nutrition and progress reports
- [ ] **Recipe Recommendations** - ML-based personalized suggestions
- [ ] **Grocery Store Integration** - Direct shopping list fulfillment

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

---

**Built with ❤️ by Krishna Joshi**  
[LinkedIn](https://linkedin.com/in/krishnajoshi28) | [Portfolio](https://krishnasportfolio23.netlify.app)
