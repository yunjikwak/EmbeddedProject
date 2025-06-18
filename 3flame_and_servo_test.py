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

# --- Global variable to track overall flame status ---
# This helps to avoid spamming "Fire not detected" messages.
# True if any flame is currently detected, False otherwise.
any_flame_detected_overall = False

# --- Flame Detection Callback Functions ---
def flame_left_detected(channel):
    global any_flame_detected_overall
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Left flame detected! Moving servo to 45 degrees.")
        set_servo_angle(45)
        any_flame_detected_overall = True
    else: # Flame gone (Active HIGH)
        print("Left flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)
        # Re-check if other flames are still detected, if not, set to False
        if not (GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW or GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW):
            any_flame_detected_overall = False


def flame_center_detected(channel):
    global any_flame_detected_overall
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Center flame detected! Moving servo to 90 degrees.")
        set_servo_angle(90)
        any_flame_detected_overall = True
    else: # Flame gone (Active HIGH)
        print("Center flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)
        # Re-check if other flames are still detected, if not, set to False
        if not (GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW or GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW):
            any_flame_detected_overall = False


def flame_right_detected(channel):
    global any_flame_detected_overall
    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        print("Right flame detected! Moving servo to 135 degrees.")
        set_servo_angle(135)
        any_flame_detected_overall = True
    else: # Flame gone (Active HIGH)
        print("Right flame gone. Moving servo to center (90 degrees).")
        set_servo_angle(90)
        # Re-check if other flames are still detected, if not, set to False
        if not (GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW or GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW):
            any_flame_detected_overall = False

# --- Event Detection Setup ---
GPIO.add_event_detect(FLAME_LEFT_PIN, GPIO.BOTH, callback=flame_left_detected, bouncetime=300)
GPIO.add_event_detect(FLAME_CENTER_PIN, GPIO.BOTH, callback=flame_center_detected, bouncetime=300)
GPIO.add_event_detect(FLAME_RIGHT_PIN, GPIO.BOTH, callback=flame_right_detected, bouncetime=300)

# --- Main Loop ---
try:
    print("Starting Raspberry Pi flame detection and servo control (event-based)...")
    set_servo_angle(90) # Set initial servo position to center

    last_print_time = time.time() # To control the frequency of "Fire not detected" message
    print_interval = 5 # Print "Fire not detected" every 5 seconds if no fire

    while True:
        # Check overall flame status if no flame was previously detected
        # and it's time to print the message again.
        if not any_flame_detected_overall and (time.time() - last_print_time > print_interval):
            print("Fire not detected.")
            last_print_time = time.time()

        time.sleep(0.1) # Check sensors every 0.1 seconds (main loop still runs)

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    servo_pwm.stop() # Stop PWM
    GPIO.cleanup()   # Clean up GPIO pins
    print("Resources cleaned up. Program exited.")
