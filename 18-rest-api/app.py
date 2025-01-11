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

from datetime import datetime

# Imports for Flask-RESTful
from flask_restful import Resource, Api

# Define Flask App
app = Flask(__name__)

api = Api(app)

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)

    def __init__(self, name, status, due_date=datetime(2099, 12, 31)):
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
    
    
###### Flask-RESTful ######
# New Resource Class for Task
class TaskResource(Resource):
    
    def get(self, task_id): 
        ''' GET: Returns Task details by Task ID'''

        task = db.session.query(Task).filter_by(id=task_id).first()
        if task is None:
            return {"message": f"Task not found for the task id {task_id}"}, 404
        else:
            return {
                "task_id": task.id, 
                "name": task.name, 
                "status": task.status, 
                "due_date": task.due_date.isoformat()
                }, 200
        
    def post(self): 
        ''' POST: Creates new Task with provided task details in the request body'''
        
        # Get Request Data
        request_data = request.json
        
        # Task Name - Required Argument
        if "name" not in request_data:
            return {"message": "Missing 'Task Name' in the request body"}, 400
        else:
            task_name = request_data['name']            

        # Due Date: Optional Arguments - use Default value
        # Additional checks can get done here, like verifying date format, and if it is not correct then send back error message
        due_date = request_data.get('due_date', datetime(9999, 12, 31))
        
        # Create new Task
        task = Task(name = task_name, due_date=datetime.strptime(due_date, "%Y-%m-%d"), status=False)
        db.session.add(task)
        db.session.commit()
        
        # Return successful message, with new task ID and any addiditional data as needed
        return {
            "message": "New task created Successfully!",
            "task_id": task.id
        }, 201
    
    def put(self, task_id): 
        ''' PUT: Update an existing Task'''
        
        task = db.session.query(Task).filter_by(id=task_id).first()
        if task is None:
            return {"message": f"Task not found for the task id {task_id}"}, 404
        else:
            # Update Exisiting Task
            # Get Request Data
            request_data = request.json
            updates_found = False
            if "name" in request_data:
                # Update Task name
                task.name = request_data['name']
                updates_found = True
            if "due_date" in request_data:
                # Update Due Date
                task.due_date = datetime.strptime(request_data['due_date'], "%Y-%m-%d")
                updates_found = True
            if "status" in request_data:
                # Update Task name
                task.status = request_data['status']
                updates_found = True
            # If Updates found in the request body, then update DB
            if updates_found:
                db.session.commit()
                return {
                    "message": f"Task with id {task_id} updated Successfully!"
                }
            else:
                return {
                    "message": f"No Updates were found in the Request Body for task with id {task_id}",
                }, 400
    
    def delete(self, task_id): 
        ''' DELETE: Delete Tasks using Task ID'''
        task = db.session.query(Task).filter_by(id=task_id).first()
        if task is None:
            return {"message": f"Task not found for the task id {task_id}"}, 404
        else:
            db.session.delete(task)
            db.session.commit()
            return {
                "message": f"Task with id {task_id} deleted Successfully!", 
                }, 200
        
# Add resource to the API
api.add_resource(TaskResource, "/task/<string:task_id>", "/task/")

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
    app.run(debug=True, port=5001)
