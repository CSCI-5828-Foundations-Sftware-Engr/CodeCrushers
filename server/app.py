from flask import Flask,render_template,request
import pika
import os, sys

from flask import Flask, render_template, url_for, request, redirect, session
from firebase import Firebase
import pyrebase

app = Flask(__name__)
app.secret_key = "notasecretkey"
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
firebaseData.initialize("firebase_cfg.json")


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
    if 'user' in session.keys():
        user_removed = session.pop('user')
        print("Logged out user: " + user_removed)

    return render_template('home.html')


@app.route('/browse', methods=['GET'])
def browse():
    # Request data from firebase.py, get list of dictionaries
    count = request.args.get('count')
    course_names = firebaseData.get_course_names(count)
    course_list = []
    for i, name in enumerate(course_names):
        course_list.append(firebaseData.get_course_by_id(name, 0))
        course_list[i]['index'] = 0

    return render_template('browse.html', data=course_list)


@app.route('/course', methods=['GET','POST'])
def course():
    flag = 0
    if request.method == "POST":
        comment = request.form['comment']
        command = f'curl localhost:5000/add-job/{comment}'
        res = os.system(command)
        print("RES: ", res)
        name = request.form['course_name']
        index = 0
        flag = 1
        course_json = firebaseData.get_course_by_id(name, index)
        comments = firebaseData.get_course_by_id(name, index)['Comments']
        print(comment)
        comments.append(comment)
        firebaseData.ref.child(name+'/').child('0/').child("Comments/").set(comments)
        

    if flag == 0:
        name = request.args.get('name').strip('"')
        index = request.args.get('id')
    ## RETRIEVE COMMENTS FOR COURSE_NAME
    ## comments = firbase_dictionary['comments']


        course_json = firebaseData.get_course_by_id(name, index)
        comments = course_json['Comments']
        #print(comments)
    return render_template('course.html', data=course_json, comments=comments)


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/index', methods=['GET', 'POST'])
def index():
    #if request.method == 'POST':
        # Get the data from the form
        #data = request.form['data']
       # print("DATAAAAAA: ", data)
      #  command = f'curl localhost:5000/add-job/{data}'
        # Run the curl command
     #   try:
    #        res = os.system(command)
   #         print("RES: ", res)
  #          print("EXECUTED command")
 #       except:
#            print("NOT FOUNDDDDDDDDDDDDDD")
        # Return a success message
        
return render_template("index.html")


@app.route('/add-job/<cmd>')
def add(cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return " [x]The comment posted is: %s" % cmd


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
