import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Firebase:

    def __init__(self):
        self.cred = None
        self.ref = None

    def initialize(self):

        print('Initializing firebase...')

        # Fetch the service account key JSON file contents
        self.cred = credentials.Certificate("codecrushers-83ba1-90965a1b9d84.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://codecrushers-83ba1-default-rtdb.firebaseio.com'
        })

        # Get a database reference to the Firebase Realtime Database
        self.ref = db.reference('/')

    def get_children(self):
        return self.ref.get()
    
    def get_course_details(self, coursename, term, year):

        children = self.get_children()
        for child in children:
            if child['Crse Title'] == coursename and child['Term'] == term and child['Year'] == int(year):
                print(child)
                return child