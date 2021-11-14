import pyrebase 
import time
import subprocess


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

def say(text):
  subprocess

def sendtext(username, message):
  ltime = db.child("time").get().val() + 1
  data={"text": message}
  db.child(username).set(data) #sends text, other user needs username to pull texts from user
  db.child("time").set(ltime)


def grabtext(username):
  ptime = 0
  while True:
    time.sleep(4)  
    ltime = db.child("time").get().val()  
    if ltime != ptime:
      message = list(db.child(username).get().val().values())[0]
      if message != "":
        print(message)
        say(message)

