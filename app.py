import json

from firebase import firebase
from flask import Flask,render_template

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://gevs-e6e1e-default-rtdb.firebaseio.com/', None)

@app.route('/')
def index():  # put application's code here
    result = firebase.get('/Voters', None)
    return render_template("index.html",jsonfile=json.dumps(result))

if __name__ == '__main__':
    app.run()
