from flask import Flask,render_template, request, jsonify
from fse_firebase import *

app = Flask(__name__)

# Initialize firebase
firebase = Firebase()
firebase.initialize()

# Get coursenames
@app.route('/getcourses', methods = ['GET'])
def getcourses():
    
    if request.method == 'GET':
        
        # Read arguments
        count = request.args.get('count').strip('"')

        # Get course list
        courseNames = firebase.get_course_names(count)
        return jsonify(courseNames)
    
# Get course history
@app.route('/coursehistory', methods = ['GET'])
def coursehistory():
    
    if request.method == 'GET':
        
        # Read arguments
        name = request.args.get('name').strip('"')

        # Get course history
        courseHistory = firebase.get_course_history(name)
        return jsonify(courseHistory)

# Specific course details
@app.route('/coursedetails', methods = ['GET'])
def coursedetails():
    
    if request.method == 'GET':
        
        # Read arguments
        name = request.args.get('name').strip('"')
        term = request.args.get('term').strip('"')
        year = request.args.get('year')

        # Get course details
        details = firebase.get_course_details(name, term, year)
        return jsonify(details)

# Get course by ID
@app.route('/courseid', methods = ['GET'])
def coursebyid():
    
    if request.method == 'GET':
        
        # Read arguments
        courseID = request.args.get('val').strip('"')

        # Get course details by ID
        details = firebase.get_course_by_id(courseID)
        return jsonify(details)
    
# Error handling
@app.errorhandler
def error_handling():
    return None

# Run the flask app
app.run()