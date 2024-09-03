from myapp import app
from flask import render_template

# Entry Point of your Website
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')