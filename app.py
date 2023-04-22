from flask import Flask, render_template, url_for, request, redirect, session
from server.fse_firebase import Firebase
import pyrebase

app = Flask(__name__)
app.secret_key = "notasecretkey"
# app.secret_key = 'pqQDrTDkEpBB8SI6rUrbclwf72TgjW3Dx0VrPObF'
# config = {
#     'apiKey': "AIzaSyARXlOfe51cqe05FTXqGenBHVMn4d52hk4",
#     'authDomain': "code-crushers-84671.firebaseapp.com",
#     'projectId': "code-crushers-84671",
#     'storageBucket': "code-crushers-84671.appspot.com",
#     'messagingSenderId': "1053885338598",
#     'appId': "1:1053885338598:web:016ba75c29b3124cba7c27",
#     'measurementId': "G-LXN6NP5MHW",
#     'databaseURL': ''
# }
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
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

firebaseData = Firebase()
firebaseData.initialize("server/codecrushers-83ba1-90965a1b9d84.json")


@app.route('/', methods=['POST', 'GET'])
def home():
    # Always render home template
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # if firebase.login_user(email, password):
            #     session['user'] = email
            # else:
            #     assert False, "Could not log in, incorrect password."
            return render_template('home.html')
        except Exception as e:
            print(e)
            return '<a href="/login">There was a problem with logging in, or the user was ' \
                   'not a valid user. Return to login.</a>'

    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            print("Got email:" + email)
            password = request.form.get('password')
            print("Got password:" + password)
            new_user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return render_template('home.html')
        except Exception as e:
            return render_template('signup.html', )
            print(e)
            return '<a href="/signup">There was a problem with signing up. Return to signup.</a>'

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session['user']:
        user_removed = session.pop('user')
        print("Logged out user: " + user_removed)

    return render_template('home.html')


@app.route('/browse', methods=['GET'])
def browse():
    # Request data from firebase, get list of JSON objects

    # Here's some dummy data
    course_json = ['Fundamentals of Software Engineering', 'Advanced Graphics',
                   'Biologically-inspired Multi-agent Systems']

    return render_template('browse.html', data=course_json)


@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')


if __name__ == '__main__':
    app.run(debug=True)
