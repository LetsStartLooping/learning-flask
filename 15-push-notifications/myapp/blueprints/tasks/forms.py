# Imports Releated to Flask WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField
from wtforms.validators import InputRequired, Length

from datetime import datetime


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