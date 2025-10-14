# main.py

import cv2
from detection import setup_device, load_yolo_model, process_frame
from control import setup_serial_connection, move_forward, move_backward, turn_left, turn_right, stop

def main(source):
    # Initialize device and model
    device = setup_device()
    model = load_yolo_model(device)

    # Initialize serial connection with Arduino
    ser = setup_serial_connection()

    # Check if the source is a video file, image, or camera
    if isinstance(source, str):  # This is a file path (image or video)
        if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Process a single image
            frame = cv2.imread(source)
            if frame is None:
                print(f"Error: Unable to read image {source}")
                return
            detected_objects = process_frame(model, frame)
            cv2.imshow('Processed Image', frame)
            cv2.waitKey(0)  # Wait for a key press to close the image window
        else:
            # Process a video file
            cap = cv2.VideoCapture(source)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                detected_objects = process_frame(model, frame)
                # Display the frame
                cv2.imshow('Frame', frame)

                # Example control logic based on detected objects
                if 'solar panel' in detected_objects:  # Customize based on detected object
                    move_forward(ser)
                else:
                    stop(ser)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
    else:
        # Camera feed (default '0' for webcam)
        cap = cv2.VideoCapture(source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from camera.")
                break
            detected_objects = process_frame(model, frame)
            cv2.imshow('Frame', frame)

            # Example control logic based on detected objects
            if 'solar panel' in detected_objects:
                move_forward(ser)
            else:
                stop(ser)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()

    cv2.destroyAllWindows()
    ser.close()  # Close serial connection after program ends

if __name__ == "__main__":
    main(source="testing.mp4")  
