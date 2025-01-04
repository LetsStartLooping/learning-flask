from myapp import app
from flask import render_template, request, jsonify
from dotenv import load_dotenv, set_key
import os

load_dotenv()

# Entry Point of your Website
@app.route('/')
def index():
    return render_template('index.html', PUBLIC_VAPID_KEY=os.getenv('PUBLIC_KEY'))

# Gets called when User subscribe to a notification
# Saves the Notification information into the DB
@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription_info = request.json
    print("\n Subscription Info \n")
    print(subscription_info)
    
    # Add Subscription Information to you DB
    # To test here it is just added to and env file
    set_key(dotenv_path=".env", key_to_set='ENDPOINT', value_to_set=subscription_info['endpoint'])
    set_key(dotenv_path=".env", key_to_set='P256DH_KEY', value_to_set=subscription_info['keys']['p256dh'])
    set_key(dotenv_path=".env", key_to_set='AUTH_KEY', value_to_set=subscription_info['keys']['auth'])
    
    return jsonify({'message': 'Subscription successful'}), 201

if __name__ == '__main__':
    app.run( debug=True, port=5003, host='0.0.0.0')