import pyrebase
import os
import json
from datetime import datetime


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


def load_medicines_for_user(uid, id_token, year, month):
    result = db.child('users').child(uid).child('medicines').get(id_token)
    data_by_date = {}

    if result.each():
        for item in result.each():
            value = item.val()
            date_str = value['date']
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date.year == year and date.month == month:
                pill = {'medicine_name': value['medicine_name'], 'quantity': value['quantity'], 'note': value['note']}
                if date_str not in data_by_date:
                    data_by_date[date_str] = []
                data_by_date[date_str].append(pill)

    return data_by_date