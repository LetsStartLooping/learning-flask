from pywebpush import webpush, WebPushException
import os
import time
from dotenv import load_dotenv
import json

load_dotenv()

def send_push_notification(title, message):
    
    VAPID_PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    # Get Subscription Info from .env file or from DB where it is stored.
    subscription_info = {
        'endpoint': os.getenv('ENDPOINT'),
        'keys': {
            'p256dh': os.getenv('P256DH_KEY'), 
            'auth': os.getenv('AUTH_KEY')
            }
        }
    try:
        # This claim identifies the sender of the Push Notification
        # Liberary `pywebpush` uses this to generate a JWT token for the push notification
        # Which is singed by VAPID Private Key
        vapid_claims = {
            'sub': 'mailto:abcd@gmail.com',  # Your email or domain
            'exp': int(time.time()) + 12 * 60 * 60  # 12 hours expiration time
        }
        
        # Send Push notification using `webpush` method of library `pywebpush`
        response = webpush(
            subscription_info=subscription_info,
            data=json.dumps({"body": message, "title": title}),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=vapid_claims
        )
        print("Notification sent successfully:", response)
        return 201
    except WebPushException as ex:
        print("Notification failed:", repr(ex))

        if ex.response is not None:
            return ex.response.status_code
        else:
            print(f"Failed to send push notification: {ex}")
            return -1
        
if __name__ == '__main__':
    send_push_notification("Test Notification", "Hi! there! This is a notification from Flask Server!")