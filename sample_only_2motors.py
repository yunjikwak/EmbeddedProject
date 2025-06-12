# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# --- Motor State Constants ---
STOP = 0
FORWARD = 1
BACKWARD = 2

# --- Motor Channel Constants ---
CH2 = 1 # Only Channel 2 used

# --- Pin Definitions (BCM Mode) ---
ENB = 19     # PWM pin for Channel 2 (OUT3,4)
IN3 = 5      # Direction pin 1
IN4 = 6      # Direction pin 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup_motor_pins(EN_PIN, INA_PIN, INB_PIN):
    GPIO.setup(EN_PIN, GPIO.OUT)
    GPIO.setup(INA_PIN, GPIO.OUT)
    GPIO.setup(INB_PIN, GPIO.OUT)
    pwm_obj = GPIO.PWM(EN_PIN, 100)
    pwm_obj.start(0)
    return pwm_obj

def set_motor_control(pwm_obj, INA_PIN, INB_PIN, speed, stat):
    pwm_obj.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA_PIN, GPIO.HIGH)
        GPIO.output(INB_PIN, GPIO.LOW)
    elif stat == BACKWARD:
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.HIGH)
    elif stat == STOP:
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.LOW)
        pwm_obj.ChangeDutyCycle(0)

# --- Main Code Execution ---
# Only Channel 2 (OUT3, OUT4) setup
pwm_ch2 = setup_motor_pins(ENB, IN3, IN4)

print("Starting single motor control (OUT3, OUT4 only)...")

try:
    set_motor_control(pwm_ch2, IN3, IN4, 70, FORWARD)
    print("Moving forward for 5 seconds (speed 70%)")
    time.sleep(5)

    set_motor_control(pwm_ch2, IN3, IN4, 40, BACKWARD)
    print("Moving backward for 5 seconds (speed 40%)")
    time.sleep(5)

    set_motor_control(pwm_ch2, IN3, IN4, 100, BACKWARD)
    print("Moving backward for 5 seconds (speed 100%)")
    time.sleep(5)

    set_motor_control(pwm_ch2, IN3, IN4, 0, STOP)
    print("Motor stopped")
    time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram termination requested by user...")

finally:
    print("Cleaning up resources...")
    set_motor_control(pwm_ch2, IN3, IN4, 0, STOP)
    pwm_ch2.stop()
    GPIO.cleanup()
