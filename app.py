from flask import Flask, render_template, url_for, request, redirect, session
import pyrebase
app=Flask(__name__)
config={
    'apiKey': "AIzaSyARXlOfe51cqe05FTXqGenBHVMn4d52hk4",
    'authDomain': "code-crushers-84671.firebaseapp.com",
    'projectId': "code-crushers-84671",
    'storageBucket': "code-crushers-84671.appspot.com",
    'messagingSenderId': "1053885338598",
    'appId': "1:1053885338598:web:016ba75c29b3124cba7c27",
    'measurementId': "G-LXN6NP5MHW",
    'databaseURL':''
}
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()

@app.route('/', methods=['POST','GET'])
def login():
    if('user' in session):
        return 'Hi ,{}'.format(session['user'])
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = auth.sign_in_with_email_and_password(email,password)
        session['user'] = email
        return redirect('\home')
        return render_template('login.html')

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        try:
            email=request.form.get('email')
            password=request.form.get('password')
            new_user = auth.create_user_with_email_and_password(email,password)
            return redirect('/')
        except:
            return 'Cant sign in'
    
    return render_template('signup.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
    x=session.pop('user')
    print(x)
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)