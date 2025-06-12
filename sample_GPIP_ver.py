# -*- coding: utf-8 -*-

# Import RPi.GPIO library for GPIO control
import RPi.GPIO as GPIO
import time # Time library for delays

# --- Motor State Constants ---
STOP = 0        # Motor stop
FORWARD = 1     # Motor forward (clockwise/counter-clockwise, depending on wiring)
BACKWARD = 2    # Motor backward (reverse direction)

# --- Motor Channel Constants ---
CH1 = 0 # First motor channel (e.g., Left motor)
CH2 = 1 # Second motor channel (e.g., Right motor)

# --- Pin Definitions (BCM Mode) ---
# L298N ENA/ENB pins (for PWM speed control)
ENA = 26 # GPIO 12 (PWM-capable pin)
ENB = 19 # GPIO 13 (PWM-capable pin)

# L298N IN1/IN2/IN3/IN4 pins (for motor direction control)
IN1 = 24 # IN1 for Channel 1 (e.g., Left motor)
IN2 = 23 # IN2 for Channel 1
IN3 = 5 # IN3 for Channel 2 (e.g., Right motor)
IN4 = 6 # IN4 for Channel 2

# --- GPIO Library Setup ---
GPIO.setmode(GPIO.BCM)      # Use BCM GPIO numbering
GPIO.setwarnings(False)     # Disable GPIO warnings

# --- Motor Pin Setup Function ---
# Sets up GPIO pins and creates a PWM object for motor speed control.
def setup_motor_pins(EN_PIN, INA_PIN, INB_PIN):
    GPIO.setup(EN_PIN, GPIO.OUT)  # Set EN pin as output
    GPIO.setup(INA_PIN, GPIO.OUT) # Set INA pin as output
    GPIO.setup(INB_PIN, GPIO.OUT) # Set INB pin as output
    
    # Create PWM object: 100Hz frequency (suitable for motor control)
    pwm_obj = GPIO.PWM(EN_PIN, 100)
    pwm_obj.start(0) # Start PWM with 0% duty cycle (motor stopped)
    return pwm_obj # Return the created PWM object

# --- Motor Control Function ---
def set_motor_control(pwm_obj, INA_PIN, INB_PIN, speed, stat):
    # Set motor speed (PWM duty cycle)
    # 'speed' should be a value from 0 to 100 (0% to 100%)
    pwm_obj.ChangeDutyCycle(speed)

    # Set motor direction
    if stat == FORWARD: # Move forward
        GPIO.output(INA_PIN, GPIO.HIGH)
        GPIO.output(INB_PIN, GPIO.LOW)
    elif stat == BACKWARD: # Move backward
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.HIGH)
    elif stat == STOP: # Stop motor
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.LOW)
        # Ensure motor speed is also set to 0 for a definite stop
        pwm_obj.ChangeDutyCycle(0)

# --- Motor Control Wrapper Function ---
# A wrapper to simplify motor control calls by channel.
def set_motor(ch, speed, stat):
    if ch == CH1: # Control the first motor
        set_motor_control(pwm_ch1, IN1, IN2, speed, stat)
    else: # Control the second motor
        set_motor_control(pwm_ch2, IN3, IN4, speed, stat)

# --- Main Code Execution ---
# Set up motor pins and create PWM objects for each channel
pwm_ch1 = setup_motor_pins(ENA, IN1, IN2)
pwm_ch2 = setup_motor_pins(ENB, IN3, IN4)

print("Starting motor control...")

try:
    # --- Control Sequence ---

    # Move forward at 70% speed
    # RPi.GPIO PWM duty cycle is 0-100. Original 150 scaled down to 70.
    set_motor(CH1, 70, FORWARD) 
    set_motor(CH2, 70, FORWARD)
    print("Moving forward for 5 seconds (speed 70%)")
    time.sleep(5) # Wait for 5 seconds

    # Move backward at 40% speed
    set_motor(CH1, 40, BACKWARD) 
    set_motor(CH2, 40, BACKWARD)
    print("Moving backward for 5 seconds (speed 40%)")
    time.sleep(5)

    # Move backward at 100% speed
    # Original 250 is scaled to 100 as max duty cycle is 100.
    set_motor(CH1, 100, BACKWARD) 
    set_motor(CH2, 100, BACKWARD)
    print("Moving backward for 5 seconds (speed 100%)")
    time.sleep(5)

    # Stop motors
    set_motor(CH1, 0, STOP) # Set speed to 0 for stop
    set_motor(CH2, 0, STOP)
    print("Motors stopped")
    time.sleep(1) # Short delay to confirm stop

except KeyboardInterrupt:
    print("\nProgram termination requested by user...")

finally:
    # --- Cleanup on Exit ---
    print("Cleaning up resources...")
    # Ensure all motors are stopped
    set_motor(CH1, 0, STOP)
    set_motor(CH2, 0, STOP)
    
    # Stop PWM objects
    pwm_ch1.stop
    pwm_ch2.stop
    GPIO.cleanup()
