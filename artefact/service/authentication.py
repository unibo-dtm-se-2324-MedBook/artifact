import pyrebase
import os
import json
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
import pickle
import os


SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", ".secrets/service_account.json")
credential = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(credential)

FIREBASE_CONFIG_FILE = os.environ.get("FIREBASE_CONFIG_FILE", ".secrets/firebase.json")
firebaseConfig = json.load(FIREBASE_CONFIG_FILE)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Check
DB_EMAIL = os.environ.get("DB_EMAIL")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

if not all([DB_EMAIL, DB_PASSWORD, DB_USERNAME]):
    raise Exception("Some DB_ envrionment variable is unset")

# firebase_auth.create_user(
#     email=DB_EMAIL,
#     password=DB_PASSWORD,
#     display_name=DB_USERNAME)

def create_user(name, surname, email, password):
  try:
    user = firebase_auth.create_user(
      email = email,
      password = password,
      display_name = name + '_' + surname)
    return user.uid # return user credentials [there is column in firebase database of users]
  except:
    return None

def login_user(email, password):
  try:
    user = auth.sign_in_with_email_and_password(email, password)
    return user['idToken']
  except:
    return None

# Save user['idToken']
def store_token(token):
  if os.path.exists('token.pickle'):
    os.remove('token.pickle')
  with open('token.pickle', 'wb') as f:
    pickle.dump(token, f)

# Exit the account
def revoke_token(token):
  firebase_auth.revoke_refresh_tokens(token)