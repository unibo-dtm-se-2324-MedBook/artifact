import pyrebase
import os
import json

FIREBASE_CONFIG_FILE = os.environ.get("FIREBASE_CONFIG_FILE", ".secrets/firebase.json")
with open(FIREBASE_CONFIG_FILE) as f:
  firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def save_pill_database(uid, id_token, medicine, quantity, date, note):
    db.child('users').child(uid).child('medicines').push(
        {
            'medicine_name': medicine,
            'quantity': quantity,
            'date': date, 
            'note': note
        },
        id_token
    )