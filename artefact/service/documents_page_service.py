from firebase_admin import storage
from service.database import db
import os
import uuid


def upload_user_document(uid: str, token: str, file_path: str):
    file_name = os.path.basename(file_path)
    unique_name = f'{uid}/{uuid.uuid4()}_{file_name}' # function from the uuid module that generates a random UUID version 4. Use it for a unique file name

    bucket = storage.bucket()
    blob = bucket.blob(unique_name)
    blob.upload_from_filename(file_path)
    blob.make_public()

    public_url = blob.public_url

    db.reference(f'documents/{uid}').push({
        'name': file_name,
        'url': public_url,
        'storage_path': unique_name
    })