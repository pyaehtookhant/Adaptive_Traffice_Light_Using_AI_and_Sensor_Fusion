import cv2
import numpy as np

def split_lanes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Define the region of interest (ROI) where the lanes are located
    height, width = edges.shape[:2]
    roi_vertices = np.array([[(0, height), (width // 2, height // 2), (width, height)]], dtype=np.int32)
    roi_mask = np.zeros_like(edges)
    cv2.fillPoly(roi_mask, roi_vertices, 255)
    roi_edges = cv2.bitwise_and(edges, roi_mask)
    
    # Perform Hough line transformation to detect lane lines
    lines = cv2.HoughLinesP(roi_edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=50)
    
    # Split the lanes based on their slopes
    left_lane_pts = []
    right_lane_pts = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        
        if slope < 0:  # Left lane
            left_lane_pts.append((x1, y1))
            left_lane_pts.append((x2, y2))
        else:  # Right lane
            right_lane_pts.append((x1, y1))
            right_lane_pts.append((x2, y2))
    
    # Create blank images to draw the lanes
    lane_image = np.zeros_like(image)
    left_lane_image = np.zeros_like(image)
    right_lane_image = np.zeros_like(image)
    
    # Draw the left lane on its corresponding image
    if left_lane_pts:
        left_lane_pts = np.array(left_lane_pts)
        cv2.polylines(left_lane_image, [left_lane_pts], isClosed=False, color=(0, 0, 255), thickness=5)
    
    # Draw the right lane on its corresponding image
    if right_lane_pts:
        right_lane_pts = np.array(right_lane_pts)
        cv2.polylines(right_lane_image, [right_lane_pts], isClosed=False, color=(0, 0, 255), thickness=5)
    
    # Combine the lane images into a single output image
    lane_image = cv2.addWeighted(left_lane_image, 1.0, right_lane_image, 1.0, 0.0)
    
    return left_lane_image, right_lane_image, lane_image

# Read the input image
image = cv2.imread('road_image.jpg')

# Split the lanes
left_lane, right_lane, lanes = split_lanes(image)

# Display the result
cv2.imshow('Left Lane', left_lane)
cv2.imshow('Right Lane', right_lane)
cv2.imshow('Lanes', lanes)
cv2.waitKey(0)
cv2.destroyAllWindows()
