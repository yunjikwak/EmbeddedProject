import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
FLAME_LEFT_PIN = 2
FLAME_CENTER_PIN = 3
FLAME_RIGHT_PIN = 4

# Servo Motor (Connected directly to Raspberry Pi GPIO, hardware PWM pin recommended)
SERVO_PIN = 12

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)   
GPIO.setwarnings(False)     # Disable GPIO warnings
GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

# --- Servo Motor Setup ---
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# --- Functions ---
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3) # Give servo time to move

def read_flame_sensors():
    left = GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW
    center = GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW
    right = GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW
    return left, center, right

def set_servo_angle_to_flame(left_detected, center_detected, right_detected):
    if center_detected:
        print("🔥 Center flame detected! Servo to 90 degrees.")
        set_servo_angle(90)
    elif left_detected and not right_detected:
        print("🔥 Left flame detected! Servo to 45 degrees.")
        set_servo_angle(45)
    elif right_detected and not left_detected:
        print("🔥 Right flame detected! Servo to 135 degrees.")
        set_servo_angle(135)
    elif left_detected and right_detected: # Both left/right (implies center or wide flame)
        print("🔥 Both sides detected! Servo to 90 degrees.")
        set_servo_angle(90)
    else:
        # No flame detected, set servo to center
        print("✅ No flame. Servo to 90 degrees.")
        set_servo_angle(90)

# --- Main Loop ---
try:
    print("Starting Raspberry Pi flame detection and servo control...")
    set_servo_angle(90) # Set initial servo position to center

    while True:
        # Read flame sensor states
        flame_left, flame_center, flame_right = read_flame_sensors()

        # Control servo based on flame detection
        set_servo_angle_to_flame(flame_left, flame_center, flame_right)

        time.sleep(0.1) # Check sensors every 0.1 seconds

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    servo_pwm.stop() # Stop PWM
    GPIO.cleanup()   # Clean up GPIO pins
    print("Resources cleaned up.")
