import cv2
import numpy as np
import time
import threading
from ultralytics import YOLO
#load model and set device
model = YOLO('yolov8n.pt', device='gpu')
PATH_TO_JSON_FILE = 'data.txt'

count = 0

#use threading to run two cameras at once
class camThread(threading.Thread):
    def __init__(self, previewName, camID, model):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.model = model
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID, self.model)

def predict(frame, model):
    return model(frame)

def camPreview(previewName, camID, model):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False
    
    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
    
        #check for car occupancy
        if model(frame).pred[0][0] == 'car':
            print('car detected at time: {0}'.format(time.time()))   # print time of detection
            print('car detected at camera: {0}'.format(camID))   # print camera number
            print('car detected at location: {0}'.format(model(frame)[0][2]))   # print location of detection
            print('car occupancy: {0}'.format(model(frame).pred[0][3]))   # print occupancy of car  
            print('flowrate: {0}'.format(model(frame).pred[0][4]))   # print flowrate of car


            count += 1
            if count % 3 != 0:
                continue
                
        #export data as json
        import json
        data = {}
        data['detection'] = []
        data['detection'].append({
            'time': time.time(),
            'camera': camID,
            'location': model(frame).pred[0][2],
            'occupancy': model(frame).pred[0][3],
            'flowrate': model(frame).pred[0][4]

        })
        with open(PATH_TO_JSON_FILE, 'w') as outfile:
            json.dump(data, outfile)
        
        
        if cv2.waitKey(1) == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# def cloudfireConnect():
#     import firebase_admin
#     from firebase_admin import credentials
#     from firebase_admin import firestore

#     # Use a service account
#     cred = credentials.Certificate('serviceAccountKey.json')
#     firebase_admin.initialize_app(cred)

#     db = firestore.client()

#     doc_ref = db.collection(u'detection').document(u'car')

#     doc_ref.set({
#         u'time': time.time(),
#         u'camera': camID,
#         u'location': model(frame).pred[0][2],
#         u'occupancy': model(frame).pred[0][3],
#         u'flowrate': model(frame).pred[0][4]
#     })


thread1 = camThread("Camera 1", 0, YOLO('yolov8n.pt', device='gpu'))
thread2 = camThread("Camera 2", 1, YOLO('yolov8n.pt', device='gpu'))





thread1.start()
thread2.start()

print ("Exiting Main Thread")

