import pyrebase #pip dependacies: pyrebase

#auth configuration
firebaseConfig={"apiKey": "AIzaSyDr4vVZdvqv8-Kklyy-wfTE1rpNclYpvAs",

  "authDomain": "asl-bility.firebaseapp.com",

  "databaseURL": "https://asl-bility-default-rtdb.firebaseio.com",

  "projectId": "asl-bility",

  "storageBucket" : "asl-bility.appspot.com",

  "messagingSenderId": "809839587836",

  "appId": "1:809839587836:web:be5770d7b81bc057fbc279",

  "measurementId": "G-S5FSMJ3W5Z"
} 

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

def sendtext(username, message):
    data={"text":message} 
    db.child(username).set(data) #sends text, other user needs username to pull texts from user

username="coolsignguy"
message="How are you"

#sendtext(username,message)
def grabtext(username,message):
    user=db.child(username).get().val()
    print(list(user.values())[0]) #user is ordered dic, gives me text value