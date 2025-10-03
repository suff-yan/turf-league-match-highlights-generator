import cv2
import numpy as np
from ultralytics import YOLO

# Load pre-trained YOLOv8 model for player detection
model = YOLO("yolov8n.pt")  # Replace with your trained model later

# Load video
video_path = "sample_match.mp4"
cap = cv2.VideoCapture(video_path)

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_hybrid_detection.mp4', fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ===== Ball Detection (White + Circular) =====
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=50, param2=30, minRadius=5, maxRadius=50)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)      # Center

    # ===== Player Detection using YOLO =====
    results = model(frame)
    annotated_frame = results[0].plot()  # YOLO draws boxes

    # Merge YOLO annotations with ball detection
    # (ball circles already drawn on 'frame', YOLO annotations on 'annotated_frame')
    # Here, we overlay annotated_frame over frame for combined view
    combined_frame = cv2.addWeighted(frame, 0.7, annotated_frame, 0.3, 0)

    # Show frame
    cv2.imshow('Football Highlight Demo', combined_frame)
    out.write(combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
