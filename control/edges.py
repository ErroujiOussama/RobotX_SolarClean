import cv2
import RPi.GPIO as GPIO
import time

# Motor GPIO Pins
MOTOR_A_FORWARD = 17
MOTOR_A_BACKWARD = 18
MOTOR_B_FORWARD = 22
MOTOR_B_BACKWARD = 23

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_A_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_A_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_B_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_B_BACKWARD, GPIO.OUT)

def move_forward():
    GPIO.output(MOTOR_A_FORWARD, True)
    GPIO.output(MOTOR_B_FORWARD, True)

def move_backward():
    GPIO.output(MOTOR_A_BACKWARD, True)
    GPIO.output(MOTOR_B_BACKWARD, True)

def stop_motors():
    GPIO.output(MOTOR_A_FORWARD, False)
    GPIO.output(MOTOR_A_BACKWARD, False)
    GPIO.output(MOTOR_B_FORWARD, False)
    GPIO.output(MOTOR_B_BACKWARD, False)

def navigate():
    cap = cv2.VideoCapture(0)  # Open the camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and apply edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Find contours of the detected edges
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Check if any contours are detected
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Control logic based on contour position
                if cX < frame.shape[1] // 3:
                    # Turn right if the center of the contour is on the left third of the frame
                    stop_motors()
                    time.sleep(0.1)  # Short pause before turning
                    move_forward()   # Adjust motor speeds as needed for turning
                elif cX > frame.shape[1] * 2 // 3:
                    # Turn left if the center of the contour is on the right third of the frame
                    stop_motors()
                    time.sleep(0.1)  # Short pause before turning
                    move_forward()   # Adjust motor speeds as needed for turning
                else:
                    move_forward()  # Move forward if centered

        # Display the resulting frame (optional for debugging)
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    stop_motors()

try:
    navigate()
except KeyboardInterrupt:
    stop_motors()
finally:
    GPIO.cleanup()
