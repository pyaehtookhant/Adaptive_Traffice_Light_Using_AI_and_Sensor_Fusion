import cv2
from ultralytics import YOLO
import time
import supervision as sv
import argparse
import numpy as np
import cvzone
import math

def predict(frame, model):
    return model(frame)




# def parse_arguments() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description="YOLOv8 live")
#     parser.add_argument(
#         "--webcam-resolution", 
#         default=[1280, 720], 
#         nargs=2, 
#         type=int
#     )
#     args = parser.parse_args()
#     return args

#load model and set device
model = YOLO(r"E:\new git repo\adaptive-traffic-lightsa\best (1).pt")

# args = parse_arguments()
# frame_width, frame_height = args.webcam_resolution

# Create video capture objects for each camera
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

cap1.set(3, 1280)
cap1.set(4, 720)
cap2.set(3, 1280)
cap2.set(4, 720)

# define resolution
# cap1.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
# cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)    
# cap2.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
# cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# ZONE_POLYGON = np.array([
#     [0, 0],
#     [0.5, 0],
#     [0.5, 1],
#     [0, 1]
# ])

# customize the bounding box
# box_annotator = sv.BoxAnnotator(
#         thickness=2,
#         text_thickness=2,
#         text_scale=1
# )

#set polygon zone
# zone_polygon1 = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
# zone1 = sv.PolygonZone(polygon=zone_polygon1, frame_resolution_wh=tuple(args.webcam_resolution))
# zone_annotator1 = sv.PolygonZoneAnnotator(
#     zone=zone1, 
#     color=sv.Color.red(),
#     thickness=2,
#     text_thickness=4,
#     text_scale=2
# )

# zone_polygon2 = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
# zone2 = sv.PolygonZone(polygon=zone_polygon2, frame_resolution_wh=tuple(args.webcam_resolution))
# zone_annotator2 = sv.PolygonZoneAnnotator(
#     zone=zone2, 
#     color=sv.Color.blue(),
#     thickness=2,
#     text_thickness=4,
#     text_scale=2
# )

while True:
    # # Read frames from the cameras and apply YOLO object detection
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    pred1 = model(frame1, stream=True)
    pred2 = model(frame2, stream=True)
    # detections1 = sv.Detections.from_yolov8(pred1)
    # detections2 = sv.Detections.from_yolov8(pred2)
    
    # #Define lebel data
    # labels1 = [
    #     f"{model.model.names[class_id]} {confidence:0.2f}"
    #     for _, confidence, class_id, _
    #     in detections1
    # ]
    
    # labels2 = [
    #     f"{model.model.names[class_id]} {confidence:0.2f}"
    #     for _, confidence, class_id, _
    #     in detections2
    # ]
    
    # #Add label to frame
    # frame1 = box_annotator.annotate(
    #         scene=frame1, 
    #         detections=detections1, 
    #         labels=labels1
    # )
    
    # frame2 = box_annotator.annotate(
    #         scene=frame2, 
    #         detections=detections2, 
    #         labels=labels2
    # )
    
    # zone1.trigger(detections=detections1)
    # frame1 = zone_annotator1.annotate(scene=frame1) 
    
    # zone2.trigger(detections=detections2)
    # frame2 = zone_annotator2.annotate(scene=frame2)
    for r in pred1:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(frame1, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(frame1, f'{model.model.names[cls]} {conf:0.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            
    for s in pred2:
        boxes = s.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(frame2, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(frame2, f'{model.model.names[cls]} {conf:0.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)        
    # # Display the frames
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # #check for prediction of car
    pred = predict(frame1, model) + predict(frame2, model)
    if pred[0] == 'vehicle':
        print('car detected at time: {0}'.format(time.time()))
        print('car detected at location: {0}'.format(pred[0][2]))
        print('car occupancy: {0}'.format(pred[0][3]))
        print('flowrate: {0}'.format(pred[0][4]))
        
        
    # # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
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