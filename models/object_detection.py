from ultralytics import YOLO
import cv2
import numpy as np

# Load the YOLOv8 model (pre-trained on COCO dataset)
model = YOLO('yolov8n.pt')  # Use nano model for speed

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
            class_name = model.names[cls]
            detections.append({
                'class': class_name,
                'confidence': conf,
                'bbox': bbox
            })

    return detections