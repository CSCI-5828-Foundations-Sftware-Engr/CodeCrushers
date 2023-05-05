from firebase import Firebase
from flask import Flask, render_template, redirect, url_for, jsonify
import pyrebase
from collections import OrderedDict
from flask_cors import CORS

firebaseData = Firebase()
firebaseData.initialize("firebase_cfg.json")

app = Flask(__name__)
app.secret_key = "notasecretkey1"
CORS(app)
firebaseConfig = {
    'apiKey': "AIzaSyDIZ0eIPqRIN4coI_TvULQZ3m_wSXqUkZE",
    'authDomain': "codecrushers-83ba1.firebaseapp.com",
    'databaseURL': "https://codecrushers-83ba1-default-rtdb.firebaseio.com",
    'projectId': "codecrushers-83ba1",
    'storageBucket': "codecrushers-83ba1.appspot.com",
    'messagingSenderId': "611473793281",
    'appId': "1:611473793281:web:f2fa45a46286a1fed6fb00",
    'measurementId': "G-6JX1R48Z3J"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route("/analyze", methods=['GET', 'POST'])
def analyze():
    comment_counts = firebaseData.get_comments()
    for title in comment_counts.keys():
        comment_counts[title] = len(comment_counts[title])
    top_3 = sorted(comment_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    return jsonify(top_3)

@app.route('/')
def home():
    return redirect(url_for('analyze'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
