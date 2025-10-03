import cv2
import numpy as np

# Load video
video_path = "sample_match.mp4"
cap = cv2.VideoCapture(video_path)

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_ball_detected.mp4', fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define white color range in HSV
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])

    # Threshold the image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply some blur to reduce noise
    mask = cv2.GaussianBlur(mask, (7,7), 0)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=50, param2=30, minRadius=5, maxRadius=50)

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)      # Center point

    # Write frame to output
    out.write(frame)

    # Show frame (optional)
    cv2.imshow('White Ball Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
