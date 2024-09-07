# Imports for Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime

# Import db from global __init__.py
from myapp import db

# Import for UUID
import uuid

# This class which inherits `db.Model` helps us create Table in the DB
# With this we can also do CRUD DB operations
class Task(db.Model):

    # Specify Table Name
    __tablename__ = 'tasks'

    # Specify Columns
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)

    def __init__(self, name, status, due_date=datetime(2099, 12, 31)):
        self.id = str(uuid.uuid4())
        self.name = name
        self.status = status
        self.due_date = due_date