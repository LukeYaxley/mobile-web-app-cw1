import json

from firebase import firebase
from flask import Flask,render_template,request

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://gevs-e6e1e-default-rtdb.firebaseio.com/', None)
auth = firebase.authentication

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
        jsonfile = {"UVC":UVC,"Name":Name,"Const":Const,"Birthday":Birthday}
        firebase.post("/Voters",jsonfile)
        return "Your name is " + Name + UVC +Birthday
    return render_template("Register Voter.html")



if __name__ == '__main__':
    app.run()
