import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import schedule
import time
import json

cred = credentials.Certificate('codecrushers-83ba1-90965a1b9d84.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://codecrushers-83ba1-default-rtdb.firebaseio.com'
})

def update_database():

    print('Updating DB')

    # Fetch data from provider
    response = requests.get('http://127.0.0.1:5000/dataprovider')
    responseJson = json.loads(response.content)
    
    # Update in firebase
    ref = db.reference('/CourseDetails')

# Schedule the function to run every hour
schedule.every(30).minutes.do(update_database)

while True:
    schedule.run_pending()
    time.sleep(1)