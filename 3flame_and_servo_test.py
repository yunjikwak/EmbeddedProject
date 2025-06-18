import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
FLAME_LEFT_PIN = 2
FLAME_CENTER_PIN = 3
FLAME_RIGHT_PIN = 4
SERVO_PIN = 12

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up flame sensor pins as inputs
GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

# Set up servo motor pin as output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM object for servo (50Hz frequency)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0) # Start PWM with 0% duty cycle

# --- Servo Control Function ---
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3) # Give servo time to move

# --- Flame Detection Callback Functions ---
def flame_left_detected(channel):
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Left flame detected! Moving servo to 45 degrees.")
        set_servo_angle(45)
    else: # Flame gone (Active HIGH)
        print("Left flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)

def flame_center_detected(channel):
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Center flame detected! Moving servo to 90 degrees.")
        set_servo_angle(90)
    else: # Flame gone (Active HIGH)
        print("Center flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)

def flame_right_detected(channel):
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Right flame detected! Moving servo to 135 degrees.")
        set_servo_angle(135)
    else: # Flame gone (Active HIGH)
        print("Right flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)

# --- Event Detection Setup ---
# Detect both rising and falling edges to catch flame detection and disappearance
GPIO.add_event_detect(FLAME_LEFT_PIN, GPIO.BOTH, callback=flame_left_detected, bouncetime=300)
GPIO.add_event_detect(FLAME_CENTER_PIN, GPIO.BOTH, callback=flame_center_detected, bouncetime=300)
GPIO.add_event_detect(FLAME_RIGHT_PIN, GPIO.BOTH, callback=flame_right_detected, bouncetime=300)

# --- Main Loop ---
try:
    print("Starting Raspberry Pi flame detection and servo control (event-based)...")
    set_servo_angle(90) # Set initial servo position to center

    while True:
        # Main loop keeps the program running; events are handled by callbacks.
        time.sleep(1) 

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    servo_pwm.stop() # Stop PWM
    GPIO.cleanup()   # Clean up GPIO pins
    print("Resources cleaned up. Program exited.")
