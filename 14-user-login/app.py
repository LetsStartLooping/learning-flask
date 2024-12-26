# Import Flask
from flask import Flask, request, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

# Imports for Password Hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Flask Login Imports
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

# Define Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'my-secret-key-flask'

# Configure the SQLite DB - Specify Path and DB Name
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

# Define DB Instance for SQLAlchemy Operations
db = SQLAlchemy(app)
# Set-up Migrations
Migrate(app, db)

# Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
# Tell users what view to go to when they need to login.
login_manager.login_view = "login"

# Model Class for User Data
class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    # Unique ID for each user
    id = db.Column(db.Integer, primary_key=True)
    # User Name
    username = db.Column(db.String, unique=True, nullable=False)
    # Password Hash
    password_hash = db.Column(db.String(150), nullable=False)
    
    # Creation/Change Log - Optional
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    
    # Methods to handle passwords
    # Get the hashed password to be stored in the DB
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    # Get Password entered by the users against the hashed password stored in the DB
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# User Loader Callback    
@login_manager.user_loader
def load_user(user_id):
    print(f"Loading User for id {user_id}")
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="Username already exists.")

        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("register.html")

# Route: Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)  # Log the user in using Flask-Login
            next_page = request.args.get("next")  # Redirect to the next page if specified
            
            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next_page == None or not next_page[0]=='/':
                next_page = url_for('index')
            
            return redirect(next_page )

        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

# Route: Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/")
def index():
    print(current_user.is_authenticated)
    return render_template("index.html", current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')