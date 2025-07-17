import pyrebase
import os
import json
import firebase_admin
from firebase_admin.auth import UserNotFoundError
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
import pickle # “Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object) is converted back into an object hierarchy.
import os # provides functions for interacting with the operating system


SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", ".secrets/service_account.json")
credential = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(credential)

FIREBASE_CONFIG_FILE = os.environ.get("FIREBASE_CONFIG_FILE", ".secrets/firebase.json")
with open(FIREBASE_CONFIG_FILE) as f:
  firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Check
# DB_EMAIL = os.environ.get("DB_EMAIL")
# DB_USERNAME = os.environ.get("DB_USERNAME")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")

# if not all([DB_EMAIL, DB_PASSWORD, DB_USERNAME]):
#     raise Exception("Some DB_ envrionment variable is unset")

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

def check_email(email):
  try:
    pos_user = firebase_auth.get_user_by_email(email)
    print('Successfully fetched user data: {0}'.format(pos_user.uid))
    print(type(pos_user.email))
    return pos_user.email
  except UserNotFoundError:
    print('email False')
    return False 
  except Exception as e:
    print(f"Other mistake: {e}")
    return None

def login_user(email, password):
  try:
    user = auth.sign_in_with_email_and_password(email, password)
    return user['idToken']
  except:
    return None

# Activate user['idToken']
def store_token(token):
  if os.path.exists('token.pickle'):
    os.remove('token.pickle') #  method is used to delete a file path. This method can not delete a directory and if directory is found it will raise an OSError
  with open('token.pickle', 'wb') as f: # Write + Binary mode
    pickle.dump(token, f) #  to store the object data to the file

# Exit the account
def log_out(token):
  if os.path.exists('token.pickle'):
    os.remove('token.pickle')

