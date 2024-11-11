import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ultralytics import YOLO
import time

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def predict(frame, model):
    return model(frame)

#load model and set device
model = YOLO('yolov8n.pt')
# Create video capture objects for each camera
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while True:
    # # Read frames from the cameras and apply YOLO object detection
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    pred1 = model(frame1)
    pred2 = model(frame2)
    
    # # Display the frames
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # #check for prediction of car
    pred = predict(frame1, model) + predict(frame2, model)
    if pred[0][0] == 'car':
        print('car detected at time: {0}'.format(time.time()))
        print('car detected at location: {0}'.format(pred[0][2]))
        print('car occupancy: {0}'.format(pred[0][3]))
        print('flowrate: {0}'.format(pred[0][4]))
        
    
    # # putboundary box on detected object
    for i in range(len(pred1.xyxy[0])):
        cv2.rectangle(frame1, (pred1.xyxy[0][i][0], pred1.xyxy[0][i][1]), (pred1.xyxy[0][i][2], pred1.xyxy[0][i][3]), (255, 0, 0), 2)
        cv2.putText(frame1, pred1.xyxy[0][i][0], (pred1.xyxy[0][i][0], pred1.xyxy[0][i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    for i in range(len(pred2.xyxy[0])):
        cv2.rectangle(frame2, (pred2.xyxy[0][i][0], pred2.xyxy[0][i][1]), (pred2.xyxy[0][i][2], pred2.xyxy[0][i][3]), (255, 0, 0), 2)
        cv2.putText(frame2, pred2.xyxy[0][i][0], (pred2.xyxy[0][i][0], pred2.xyxy[0][i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        
    # # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # # collect car detect data and send to firebase
    if pred == 'car':
        doc_ref = db.collection(u'camera').document(u'cam1')
        doc_ref.set({
            u'car_detected': pred1[0][0],
            u'car_location': pred1[0][2],
            u'car_occupancy': pred1[0][3],
            u'flowrate': pred1[0][4]
        })
    
        doc_ref = db.collection(u'camera').document(u'cam2')
        doc_ref.set({
            u'car_detected': pred2[0][0],
            u'car_location': pred2[0][2],
            u'car_occupancy': pred2[0][3],
            u'flowrate': pred2[0][4]
        })
    
        

    print(u'Data sent to the database')
    print(f"{doc_ref.id} is created in the database  at {doc_ref.create_time}")
    # # Read frames from the cameras
    

    
    
    
    # ret1, frame1 = cap1.read()
    # ret2, frame2 = cap2.read()

    # # Display the frames
    # cv2.imshow('Camera 1', frame1)
    # cv2.imshow('Camera 2', frame2)

    # # Break the loop if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


    

# Release the video capture objects
cap1.release()
cap2.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
