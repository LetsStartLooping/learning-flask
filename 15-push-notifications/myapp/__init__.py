# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Define Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'my-secret-key-flask'
