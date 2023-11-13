# Import Flask
from flask import Flask, render_template, request

# Imports Releated to Flask WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length

# Imports for Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import for UUID
import uuid


# Define Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'my-secret-key-01'


# Configure the SQLite DB - Specify Path and DB Name
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

# Define DB Instance for SQLAlchemy Operations
db = SQLAlchemy(app)
# Set-up Migrations
Migrate(app, db)


# This class which inherits `db.Model` helps us create Table in the DB
# With this we can also do CRUD DB operations
class Task(db.Model):

    # Specify Table Name
    __tablename__ = 'tasks'

    # Specify Columns
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)

    def __init__(self, name, status):
        self.id = str(uuid.uuid4())
        self.name = name
        self.status = status


# Define Flask From for New Task
class NewTask(FlaskForm):
    name = StringField(label="New Task", validators=[InputRequired(), Length(min=5, max=40)])
    add = SubmitField(label="Add Task")
    status = SubmitField(label="Status Change")

# Entry Point of your Website
@app.route('/')
def index():
    return render_template('index.html')

# 2nd Page - Tasks
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():

    # Read Exising Tasks from DB
    my_tasks = db.session.query(Task).all()

    # Form
    form = NewTask()

    # Form Step 1: Method call Validate Submig
    if form.validate_on_submit():
        # Form Step 2: Check whether `Add` button was clicked or not
        if form.add.data:
            # Form Step 3: Get the details of new Task
            new_task_name = form.name.data

            # Create a new Task Object
            new_task = Task(name=new_task_name, status=False)

            # Add that to the db.session
            db.session.add(new_task)
            # Post commit work to add entry to the table
            db.session.commit()

            # Read Exising Tasks from DB
            my_tasks = db.session.query(Task).all()

            # Clear HTML Text Input field
            form.name.data = ""

    if request.method == 'POST':
        # Updating Task Status
        changed_task_ids = request.form.getlist("t_status")
        for task in my_tasks:
            task.status = str(task.id) in changed_task_ids

        # Update Task Status to DB
        db.session.commit()
        


    return render_template('tasks.html', my_tasks = my_tasks, form=form)

if __name__ == '__main__':

    # Run the App
    app.run(debug=True)

