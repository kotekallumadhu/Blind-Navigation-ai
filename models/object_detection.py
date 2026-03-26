from ultralytics import YOLO
import cv2
import numpy as np

# Load the YOLOv8 model (pre-trained on COCO dataset)
model = YOLO('yolov8n.pt')  # Use nano model for speed

def estimate_distance(pixel_width):
    KNOWN_WIDTH = 0.5
    FOCAL_LENGTH = 700
    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / pixel_width
    return round(distance, 2)

def detect_objects(image_bytes):
    """
    Detect objects in the image.
    :param image_bytes: Bytes of the image
    :return: List of detections with class, confidence, bbox
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run inference
    results = model(img)

    detections = []
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]

            # ADD THIS PART
            x1, y1, x2, y2 = bbox
            pixel_width = x2 - x1
            distance = estimate_distance(pixel_width)

            class_name = model.names[cls]
            detections.append({
                'class': class_name,
                'confidence': conf,
                'bbox': bbox,
                'distance': distance
           })

    return detections