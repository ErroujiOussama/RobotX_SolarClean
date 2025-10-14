import serial
import time

# Setup the serial connection to communicate with the Arduino
def setup_serial_connection(port='COM1', baudrate=9600):
    """Set up serial communication with Arduino."""
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for Arduino to initialize
    return ser

def send_command(ser, command):
    """Send a movement command to the Arduino."""
    ser.write(command.encode())
    time.sleep(0.1)  # Slight delay to prevent command spamming

def move_forward(ser):
    """Send command to move robot forward."""
    send_command(ser, "move_forward")

def move_backward(ser):
    """Send command to move robot backward."""
    send_command(ser, "move_backward")

def turn_left(ser):
    """Send command to turn robot left."""
    send_command(ser, "turn_left")

def turn_right(ser):
    """Send command to turn robot right."""
    send_command(ser, "turn_right")

def stop(ser):
    """Send command to stop the robot."""
    send_command(ser, "stop")
