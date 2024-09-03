# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask Login
from flask_login import LoginManager

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

# Flask Login
# login_manager = LoginManager()
# login_manager.init_app(app)


# TODO - Register Blueprints

from myapp.blueprints.tasks.routes import task
app.register_blueprint(task, url_prefix='/tasks')

from myapp.blueprints.users.routes import user
app.register_blueprint(user, url_prefix='/users')