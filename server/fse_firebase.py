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
        self.ref = db.reference('/CourseDetails')

    def get_children(self):
        return self.ref.get()
    
    def get_course_names(self, count):

        courseNames = []
        children = list(self.get_children().keys())

        newCount = int(count) if (int(count) < len(children)) else len(children)

        for i in range(newCount):
            courseNames.append(children[i])

        return courseNames
    
    def get_course_history(self, coursename):

        children = self.get_children()
        history = children.get(coursename, None)
        return history
    
    def get_course_details(self, coursename, term, year):

        entries = []
        children = self.get_children()

        history = children.get(coursename, None)
        if not history:
            return entries
        
        for entry in history:
            if entry["Term"] == term and entry["Year"] == int(year):
                entries.append(entry)

        return entries
    
    def get_course_by_id(self, courseID):

        children = self.get_children()

        course_id_tokens = courseID.split('-')
        coursename = ' '.join(course_id_tokens[:len(course_id_tokens) - 1])

        child = children.get(coursename, None)
        if child:
            index = int(course_id_tokens[len(course_id_tokens) - 1])
            if index < len(child):
                return child[index]
            else:
                return None
        else:
            return None