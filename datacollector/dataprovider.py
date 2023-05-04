from flask import Flask,render_template, request, jsonify
import json

app = Flask(__name__)

# Provide course details
@app.route('/dataprovider', methods = ['GET'])
def coursedetails():
    
    if request.method == 'GET':

        # Get course details
        f = open('sample.json')
        details = json.load(f)
        return jsonify(details)
    
# Error handling
@app.errorhandler
def error_handling():

    return None


# Run the flask app
app.run()