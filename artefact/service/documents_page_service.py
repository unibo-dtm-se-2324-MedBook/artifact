import pyrebase
import os
import json
from service.database import db
import uuid

FIREBASE_CONFIG_FILE = os.environ.get("FIREBASE_CONFIG_FILE", ".secrets/firebase.json")
with open(FIREBASE_CONFIG_FILE) as f:
    firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def upload_user_document(uid: str, token: str, file_path: str):
    print("upload_user_document called")
    
    file_name = os.path.basename(file_path)
    unique_name = f'{uid}/{uuid.uuid4()}_{file_name}' # function from the uuid module that generates a random UUID version 4. Use it for a unique file name
    print("Uploading file:", file_path)
    print("Unique name:", unique_name)

    # bucket = storage.bucket()
    # blob = bucket.blob(unique_name)
    # blob.upload_from_filename(file_path)
    # blob.make_public()
    # public_url = blob.public_url
    storage.child(unique_name).put(file_path, token)
    public_url = storage.child(unique_name).get_url(token)
    print("File uploaded to storage, public url:", public_url)

    db.child('users').child(uid).child('documents').push({
        'name': file_name,
        'url': public_url,
        'storage_path': unique_name
    }, token)


def load_user_documents(uid: str, token: str) -> dict:
    documents = db.child('users').child(uid).child('documents').get(token)
    return documents.val() if documents.each() else {}