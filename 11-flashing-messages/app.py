# Import Flask
from flask import Flask, render_template, request, redirect, url_for

# For Flash Messages
from flask import flash

# Imports Releated to Flask WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField
from wtforms.validators import InputRequired, Length

# Imports for Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import for UUID
import uuid

from datetime import datetime

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


# Define Flask From for New Task
class NewTask(FlaskForm):
    name = StringField(label="New Task", validators=[InputRequired(), Length(min=5, max=40)])
    add = SubmitField(label="Add Task")
    status = SubmitField(label="Status Change")

# User Form to Update Task
class EditTask(FlaskForm):
    # To edit the name of your task
    name = StringField(label="Task Name", validators=[InputRequired(), Length(min=5, max=40)])
    # To change task status
    status = BooleanField(label="Status")
    # Add a due date to our Task
    due_date = DateField(label="Due Date", default=datetime.now())
    # Update Task
    update = SubmitField(label="Update")
    # Delete Task
    delete = SubmitField(label="Delete Task")
    # Cancel and go back
    cancel = SubmitField(label="Cancel")

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

            # Flash Successful message
            flash(message="Task Added Successfully", category="success")

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

# 3rd Page: Update Task
@app.route('/update_task', methods=['GET', 'POST'])
def update_task():

    # Create User Form for Edit Task
    form = EditTask()

    # Get the Task ID (passed when user clicked on a task)
    task_id = request.args.get("task_id")

    # Get Task details
    task = db.session.query(Task).filter(Task.id == task_id).first()

    if form.validate_on_submit():

        # Handle Cancel
        if form.cancel.data:
            flash(message="No Changes were made", category="info")
            return redirect(url_for('tasks'))
        
        # Handle Delete
        if form.delete.data:
            db.session.delete(task)
            db.session.commit()
            flash(message="Task Deleted Successfully", category="warning")
            return redirect(url_for('tasks'))

        # Handle Update
        if form.update.data:
            # Read updated data from the Form
            task.name = form.name.data
            task.due_date = form.due_date.data

            db.session.commit()
            flash(message="Task updated successfully!", category="success")
            return redirect(url_for('tasks'))
        
     # Load Form Data with task details
    form.name.data = task.name
    if task.due_date == None:
        form.due_date.data = datetime(2099, 12, 31)
    else:
        form.due_date.data = task.due_date

    return render_template('update_task.html', form = form, task = task)


if __name__ == '__main__':

    # Run the App
    app.run(debug=True)

