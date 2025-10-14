import cv2

def navigate():
    cap = cv2.VideoCapture(0)  # Open the webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and apply edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Find contours of the detected edges
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize command variable
        command = "Stop"

        # Check if any contours are detected
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Control logic based on contour position
                if cX < frame.shape[1] // 3:
                    command = "Turn Right"
                elif cX > frame.shape[1] * 2 // 3:
                    command = "Turn Left"
                else:
                    command = "Move Forward"

                # Draw a marker at the center of the largest contour
                cv2.drawMarker(frame, (cX, cY), color=(0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

        # Overlay command text on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'Command: {command}', (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

try:
    navigate()
except KeyboardInterrupt:
    pass
