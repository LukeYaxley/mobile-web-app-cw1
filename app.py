import json

import firebase_admin
from firebase_admin import auth
from firebase import firebase
from flask import Flask,render_template,request
import pyrebase
app = Flask(__name__)
default_app = firebase_admin.initialize_app()

firebase = firebase.FirebaseApplication('https://gevs-e6e1e-default-rtdb.firebaseio.com/', None)
authentication = firebase.authentication

@app.route('/')
def index():  # put application's code here
    result = firebase.get('/Voters', None)
    return render_template("index.html",jsonfile=json.dumps(result))

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
        jsonfile = {"UVC":UVC,"Name":Name,"Const":Const,"Birthday":Birthday,"VoterID":VoterID}
        firebase.post("/Voters",jsonfile)
        #create user in firebase

        auth.create_user(
            email=VoterID,
            email_verified=False,
            password=Password,
            display_name=Name
            )
        return "Your name is " + Name + UVC +Birthday
    return render_template("Register Voter.html")



if __name__ == '__main__':
    app.run()
