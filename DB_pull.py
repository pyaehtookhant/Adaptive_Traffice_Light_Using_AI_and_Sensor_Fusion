import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

data = []
# Use a service account.
cred = credentials.Certificate('path/to/serviceAccount.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection(u'camera').stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')


#json conversion
import json
import numpy as np

#conver data collected from firebase to json
def firebase_to_json(data, docs):
    for doc in docs:
        data.append(doc.to_dict())
    return json.dumps(data)

#send back to firebase
def json_to_firebase(data):
    for i in range(len(data)):
        db.collection(u'merged').document(str(i)).set(data[i])




print(firebase_to_json(data))









