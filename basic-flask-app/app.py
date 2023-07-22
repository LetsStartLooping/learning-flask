from flask import Flask, render_template

# Define Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'my-secret-key'


@app.route('/')
def index1():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

