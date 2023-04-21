from flask import Flask, render_template, url_for, request, redirect, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
config = {
    'apiKey': "AIzaSyARXlOfe51cqe05FTXqGenBHVMn4d52hk4",
    'authDomain': "code-crushers-84671.firebaseapp.com",
    'projectId': "code-crushers-84671",
    'storageBucket': "code-crushers-84671.appspot.com",
    'messagingSenderId': "1053885338598",
    'appId': "1:1053885338598:web:016ba75c29b3124cba7c27",
    'measurementId': "G-LXN6NP5MHW",
    'databaseURL': ''
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['POST', 'GET'])
def home():
    # Always render home template
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if session['user']:
            email = request.form.get('email')
            password = request.form.get('password')
            # user = auth.sign_in_with_email_and_password(email, password)
            if email == session['user']:
                return render_template('home.html')
            else:
                return '<a href="/login">Not a valid user. Return to login.</a>'
        else:
            return '<a href="/login">Not a valid user. Return to login.</a>'

    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            print("Got email:" + email)
            password = request.form.get('password')
            print("Got password:" + password)
            session['user'] = email
            session['password'] = password
            # new_user = auth.create_user_with_email_and_password(email, password)
            return render_template('home.html')
        except:
            return 'Cant sign up'

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session['user']:
        user_removed = session.pop('user')
        print("Removed user: " + user_removed)

    return redirect('/')


@app.route('/browse', methods=['GET'])
def browse():
    return render_template('browse.html')


@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')


if __name__ == '__main__':
    app.run(debug=True)
