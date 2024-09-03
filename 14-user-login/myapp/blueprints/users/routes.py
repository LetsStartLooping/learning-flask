# Import Flask
from flask import render_template, request, redirect, url_for

# For Flash Messages
from flask import flash


## Import Flask App and other global paramters
from myapp import db, app

from datetime import datetime

## Import Blueprint
from flask import Blueprint

user = Blueprint('users', __name__, 
                  static_folder='static',
                  template_folder='templates'
                  )



# 2nd Page - Tasks
@user.route('/register', methods=['GET', 'POST'])
def tasks():

    

    return render_template('register.html')


