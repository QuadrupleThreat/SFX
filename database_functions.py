import pyrebase #pip dependacies: pyrebase
import keyboard
import time


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
    data={"text": message}
    db.child(username).set(data) #sends text, other user needs username to pull texts from user

username="hearing_imp"
message="How are you"
oldmessage=""
#sendtext(username,message)
def grabtext(username,oldmessage):
    while True:
      if keyboard.is_pressed('q'):
        break
      else:
        time.sleep(4)   
        if oldmessage=="":
          print(list(db.child(username).get().val().values())[0]) 
          oldmessage=list(db.child(username).get().val().values())[0] #switches message out to allow a new message to be sent

        elif list(db.child(username).get().val().values())[0]!=oldmessage:
          print(list(db.child(username).get().val().values())[0])
          oldmessage=list(db.child(username).get().val().values())[0]
          

    #print(list(user.values())[0]) #user is ordered dic, gives me text value

grabtext(username,oldmessage)
