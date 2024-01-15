import json
import secrets

import pyrebase
import Check
#import firebase_admin
from firebase import firebase
#from firebase_admin import credentials, auth
from flask import Flask, render_template, request, redirect, url_for, session

import pyrebase
import requests
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
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
            session['User'] = email
            with open("ElectionOfficers.txt","r") as f:
                officers = f.read().splitlines()
                if email in officers:
                    session['Officer'] = True
                    return redirect(url_for("Officer_Dashboard"))
            return redirect(url_for("VDashboard"))
        #catch firebase errors for if login doesn't work
        except requests.exceptions.HTTPError as e:
            error_message = "Invalid Email Address or Password"
        return render_template("index.html",message = error_message)
    else:
        return render_template("index.html")


def logout():
    session.pop('User')
    redirect('/')
@app.route('/register', methods =["GET", "POST"])
def register():
    error = None
    if request.method == "POST":

        # getting input with name = UVC in HTML form
        UVC = request.form.get("UVC")
        Name = request.form.get("Name")
        Const = request.form.get("Const")
        Birthday = request.form.get("Birthday")
        VoterID = request.form.get("VoterID")
        Password = request.form.get("Password")
        jsonfile = {"Voters/"+UVC:{"Name":Name,"Const":Const,"Birthday":Birthday,"VoterID":VoterID,"Vote":True}}
        if Check.validUVC(UVC) == True:

            #create user in firebase
            try:
                auth.create_user_with_email_and_password(VoterID,Password)
                # add voter data to db
                db.update(jsonfile)
            except requests.exceptions.HTTPError as e:
                error = json.loads(e.args[1])['error']['message']





        else:
            error = "Invalid UVC, either UVC is already in use or is not correct"

        if error != None:
            return render_template("Register Voter.html", message=error)
        else:
            return redirect(url_for("VDashboard"))
    return render_template("Register Voter.html")

@app.route('/VDashboard')
def VDashboard():
    try:
        email = session['User']
    except KeyError:
        return redirect('/')
    if db.child("Open").get().val() == True:
        voters = db.child("Voters").order_by_child("VoterID").equal_to(email).get().val()
        if next(iter(voters.values()))['Vote'] == False:
            return render_template("Thank You.html")
        Const = next(iter(voters.values()))['Const']
        Candidates = db.child('Candidates').get().val()
        Constituency_data = Candidates[int(Const)][1:]
        session['Const']= Const
        return render_template("Voter Dashboard.html",Constituency_data = Constituency_data)
    else:
        return render_template("Voting Closed.html")
@app.route('/ThankYou',methods =["GET", "POST"])
def submit_vote():
    if request.method == "POST":
        selected_candidate = request.form.get('selected_candidate').split("|")

        candidates = db.child("Candidates").child(int(selected_candidate[0]))
        Votes = candidates.get().val()[1:][0]["Votes"]
        db.child("Candidates").child(session['Const']).child(int(selected_candidate[0])).update({"Votes":(Votes+1)})

        voters = db.child("Voters").order_by_child("VoterID").equal_to(session['User'])
        UVC = next(iter(voters.get().val().keys())) #get UVC
        db.child("Voters").child(UVC).update({"Vote":False})
    return render_template("Thank You.html")

@app.route("/ODashboard",methods = ["GET","POST"])
def Officer_Dashboard():
    initial_checkbox = False
    try:
        email = session['User']
    except KeyError:
        return redirect('/')
    if request.method == "GET":
        if db.child("Open").get().val() == True:
            initial_checkbox = True

    if request.method == "POST":
        if request.form.get("Voting") == "on":
            db.update({"Open":True})
        else:
            db.update({"Open": False})
    return render_template("Officer Dashboard.html",initial_checkbox_value=initial_checkbox)
    # show voting results
if __name__ == '__main__':
    app.run()
