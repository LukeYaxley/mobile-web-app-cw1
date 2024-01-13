import json
import pyrebase

#import firebase_admin
from firebase import firebase
#from firebase_admin import credentials, auth
from flask import Flask,render_template,request

import pyrebase
import requests
app = Flask(__name__)
#default_app = firebase_admin.initialize_app()
#Pyrebase credentials
config = {
    "apiKey": "AIzaSyAuhVXUUqT8o9sLXKB0O0XyUslsRr1l8Lo",
    "authDomain": "gevs-e6e1e.firebaseapp.com",
    "databaseURL": "https://gevs-e6e1e-default-rtdb.firebaseio.com",
    "projectId": "gevs-e6e1e",
    "storageBucket": "gevs-e6e1e.appspot.com",
    "messagingSenderId": "1036800821152",
    "appId": "1:1036800821152:web:77b1a3e54e5def680486c5",
    "measurementId": "G-TKFZRTDVK2"
}

firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
#authentication = firebase.authentication
#cred = credentials.Certificate('gevs-e6e1e-firebase-adminsdk-ygkzs-c877dd098c.json')
db = firebase.database()

@app.route('/', methods =["GET", "POST"])
def login():  # put application's code here
    result = db.child("/Voters").get()
    if request.method == "POST":
        email = request.form.get("user")
        password = request.form.get("password")
        error_message = ""
        try:
            user = auth.sign_in_with_email_and_password(email, password)

        #catch firebase errors for if login doesn't work
        except requests.exceptions.HTTPError as e:
            error_message = "Invalid Email Address or Password"
        return render_template("index.html",message = error_message)
    else:
        return render_template("index.html")

@app.route('/register', methods =["GET", "POST"])
def register():
    if request.method == "POST":
        # getting input with name = UVC in HTML form
        UVC = request.form.get("UVC")
        Name = request.form.get("Name")
        Const = request.form.get("Const")
        Birthday = request.form.get("Birthday")
        VoterID = request.form.get("VoterID")
        Password = request.form.get("Password")
        jsonfile = {"Voters/"+UVC:{"Name":Name,"Const":Const,"Birthday":Birthday,"VoterID":VoterID}}

        #create user in firebase
        auth.create_user_with_email_and_password(VoterID,Password)

        #add voter data to db
        db.update(jsonfile)

        validUser(UVC,VoterID,Password)
        return "Your name is " + Name + UVC +Birthday
    return render_template("Register Voter.html")


#def validUser(UVC,VoterID,Password):


if __name__ == '__main__':
    app.run()
