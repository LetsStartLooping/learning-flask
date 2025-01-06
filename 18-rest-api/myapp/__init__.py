# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


# TODO - Register Blueprints

from myapp.tasks import task

app.register_blueprint(task, url_prefix='/tasks')