import pyrebase
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

def validUVC(UVC):
    Voters = db.child("Voters")
    ValidUVC = open("Valid UVC.txt",'r').read().splitlines()
    #check if UVC is in list of valid UVC codes imported from text file
    if UVC not in ValidUVC:
        return False
    #check UVC doesn't have children (doesn't exist)

    elif Voters.child(UVC).get().val() != None:
        return False
    else:
        return True
validUVC("VFBH8W6W")
