import firebase_admin
from firebase_admin import credentials, db


class Firebase:

    def __init__(self):
        self.cred = None
        self.ref = None

    def initialize(self, cfg_path):

        print('Initializing firebase...')

        # Fetch the service account key JSON file contents
        self.cred = credentials.Certificate(cfg_path)

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

    def get_course_list(self, num_courses):
        # This gets the entire dictionary of course names
        children = self.get_children()['CourseDetails']

        # Loop through num_courses and pull out the first entry
        courses = []
        for i, key in enumerate(children.keys()):
            if i == num_courses:
                break

            children[key][0]['index'] = '0'
            courses.append(children[key][0])

        return courses

    def get_by_course_id(self, course_id):
        # This gets the entire dictionary of course names
        children = self.get_children()['CourseDetails']

        # Separate out coursename and index from course_id
        course_id_tokens = course_id.split('-')

        coursename = ' '
        coursename = coursename.join(course_id_tokens[:len(course_id_tokens) - 1])

        # Select by coursename then index
        return children[coursename][int(course_id_tokens[len(course_id_tokens) - 1])]
