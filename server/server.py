from flask import Flask, render_template, request, jsonify
from fse_firebase import *

app = Flask(__name__)

# Initialize firebase
firebase = Firebase()
firebase.initialize()


# Login
@app.route('/coursedetails', methods=['GET'])
def coursedetails():
    if request.method == 'GET':
        # Read arguments
        name = request.args.get('name').strip('"')
        print(name)
        term = request.args.get('term').strip('"')
        print(term)
        year = request.args.get('year')
        print(year)

        # Get course details
        details = firebase.get_course_details(name, term, year)
        return jsonify(details)


# Error handling
@app.errorhandler
def error_handling():
    return None


# Run the flask app
app.run()