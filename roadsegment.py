import cv2
import numpy as np
import cvzone
import math

 
def canny(cap, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(cap, low_threshold, high_threshold)

def greyscale(cap):
    return cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

def region_of_interest(cap, vertices):
    mask = np.zeros_like(cap)
    if len(cap.shape) > 2:
        channel_count = cap.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(cap, mask)
    return masked_image



def line_draw(cap, lines, color=[255,0,0], thickness=10):
    imgshape = cap.shape
    left_x1 = []
    left_x2 = []
    right_x1 = []
    right_x2 = []

    y_min_global = imgshape[0]
    y_max_global = int(imgshape[0]*0.611)
    for line in lines:
        for x1,y1,x2,y2 in line:
            if((y2-y1)/(x2-x1)<0):
                mc = np.polyfit([x1,x2],[y1,y2],1)
                left_x1.append(int((y_min_global-mc[1])/mc[0]))
                left_x2.append(int((y_max_global-mc[1])/mc[0]))
            else:
                mc = np.polyfit([x1,x2],[y1,y2],1)
                right_x1.append(int((y_min_global-mc[1])/mc[0]))
                right_x2.append(int((y_max_global-mc[1])/mc[0]))

    l_avg_x1 = int(np.mean(left_x1))
    l_avg_x2 = int(np.mean(left_x2))
    r_avg_x1 = int(np.mean(right_x1))
    r_avg_x2 = int(np.mean(right_x2))

    cv2.line(cap, (l_avg_x1, y_min_global), (l_avg_x2, y_max_global), color, thickness)
    cv2.line(cap, (r_avg_x1, y_min_global), (r_avg_x2, y_max_global), color, thickness)

    return cap

def hough_lines(cap, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(cap, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((cap.shape[0], cap.shape[1], 3), dtype=np.uint8)
    line_draw(line_img, lines)
    return line_img

def weighted_img(cap, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, cap, β, λ)

def process_image(cap):
    cap = greyscale(cap)
    cap = canny(cap, 50, 150)
    vertices = np.array([[(0,cap.shape[0]),(cap.shape[1]*0.45, cap.shape[0]*0.611), (cap.shape[1]*0.55, cap.shape[0]*0.611), (cap.shape[1],cap.shape[0])]], dtype=np.int32)
    cap = region_of_interest(cap, vertices)
    cap = hough_lines(cap, 1, np.pi/180, 10, 20, 5)
    cap = weighted_img(cap, cap)
    return cap

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


while True:
    ret, frame = cap.read()
    frame = process_image(frame)
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
