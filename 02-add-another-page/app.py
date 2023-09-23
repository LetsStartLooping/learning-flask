# 1. Import Flask
from flask import Flask, render_template

# 2. Define Flask App
app = Flask(__name__)

# 3. Secret Key
app.config['SECRET_KEY'] = 'my-secret-key'

# 4. Entry Point of your Website
@app.route('/')
def index():
    return render_template('index.html')

# 6. 2nd Page - Tasks
@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

if __name__ == '__main__':
    # 5. Run the App
    app.run(debug=True)

