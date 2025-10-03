from ultralytics import YOLO
import cv2

# Load a pre-trained YOLOv8 model (YOLOv8n - nano version, lightweight)
model = YOLO("yolov8n.pt")  # You can replace with yolov8s.pt or your custom model later

# Load a video
video_path = "sample_match.mp4"
cap = cv2.VideoCapture(video_path)

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_detected.mp4', fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection on the frame
    results = model(frame)

    # Draw bounding boxes on detected objects
    annotated_frame = results[0].plot()  # plots boxes on the frame

    # Show frame (optional)
    cv2.imshow("Ball Detection", annotated_frame)

    # Write frame to output video
    out.write(annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
