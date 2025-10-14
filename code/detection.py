import torch
from ultralytics import YOLO
from utilis import YOLO_Detection, label_detection

def setup_device():
    """Check if CUDA is available and set the device."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    return device

def load_yolo_model(device):
    """Load the YOLO model and configure it."""
    model = YOLO("training_results/weights/best.pt")
    model.to(device)
    model.nms = 0.7  # Non-Maximum Suppression (NMS) threshold
    print(f"Model classes: {model.names}")
    return model

def process_frame(model, frame):
    """Process a single frame to detect objects and apply labels."""
    boxes, classes, names, confidences = YOLO_Detection(model, frame, conf=0.4)
    
    detected_objects = []

    for box, cls in zip(boxes, classes):
        detected_objects.append(names[int(cls)])  # Capture object names detected

        # Draw bounding boxes and labels on frame
        label_detection(frame=frame, text=f"{names[int(cls)]}", tbox_color=(255, 144, 30),
                        left=box[0], top=box[1], bottom=box[2], right=box[3])
    
    return detected_objects
