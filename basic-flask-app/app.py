from flask import Flask, render_template

# Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'my-secret-key'

@app.route('/')
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

