# Import Flask
from flask import render_template, request, redirect, url_for

# For Flash Messages
from flask import flash

# Blueprint Specific Imports
## Import Flask Forms
from myapp.forms import NewTask, EditTask

## Import Task DB
from myapp.models import Task

## Import Flask App and other global paramters
from myapp import db, app

from datetime import datetime

## Import Blueprint
from flask import Blueprint

task = Blueprint('tasks', __name__, 
                  static_folder='static',
                  template_folder='templates'
                  )



# 2nd Page - Tasks
@task.route('/', methods=['GET', 'POST'])
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
@task.route('/update_task', methods=['GET', 'POST'])
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
            return redirect(url_for('tasks.tasks'))
        
        # Handle Delete
        if form.delete.data:
            db.session.delete(task)
            db.session.commit()
            flash(message="Task Deleted Successfully", category="warning")
            return redirect(url_for('tasks.tasks'))

        # Handle Update
        if form.update.data:
            # Read updated data from the Form
            task.name = form.name.data
            task.due_date = form.due_date.data

            db.session.commit()
            flash(message="Task updated successfully!", category="success")
            return redirect(url_for('tasks.tasks'))
        
     # Load Form Data with task details
    form.name.data = task.name
    if task.due_date == None:
        form.due_date.data = datetime(2099, 12, 31)
    else:
        form.due_date.data = task.due_date

    return render_template('update_task.html', form = form, task = task)


