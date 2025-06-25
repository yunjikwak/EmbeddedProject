import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
# Flame Sensors
FLAME_LEFT_PIN = 22
FLAME_CENTER_PIN = 23
FLAME_RIGHT_PIN = 24

# Servo and Pump (from firefighting system)
SERVO_PIN = 18
PUMP_IN1 = 25
PUMP_IN2 = 8

# RC Car Motors (L298N Motor Driver)
# Right Motor
IN1_RIGHT = 17
IN2_RIGHT = 27
EN_A_RIGHT = 12
# Left Motor
IN3_LEFT = 5
IN4_LEFT = 6
EN_B_LEFT = 13

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensor Inputs
GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

# Actuator Outputs
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(PUMP_IN1, GPIO.OUT)
GPIO.setup(PUMP_IN2, GPIO.OUT)
GPIO.setup(IN1_RIGHT, GPIO.OUT)
GPIO.setup(IN2_RIGHT, GPIO.OUT)
GPIO.setup(EN_A_RIGHT, GPIO.OUT)
GPIO.setup(IN3_LEFT, GPIO.OUT)
GPIO.setup(IN4_LEFT, GPIO.OUT)
GPIO.setup(EN_B_LEFT, GPIO.OUT)


# --- PWM Objects ---
# For Servo
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# For rccar (Speed Control)
motor_pwm_right = GPIO.PWM(EN_A_RIGHT, 100)
motor_pwm_left = GPIO.PWM(EN_B_LEFT, 100)
motor_pwm_right.start(75) # speed (0-100)
motor_pwm_left.start(75)  # speed (0-100)


# --- Global Variables ---
pump_on = False
pump_start_time = 0
pump_duration = 5 # Pump active duration in seconds
state = "IDLE"

# --- rccar Control Functions ---
def move_stop():
    # print("Stop")
    GPIO.output(IN1_RIGHT, GPIO.LOW)
    GPIO.output(IN2_RIGHT, GPIO.LOW)
    GPIO.output(IN3_LEFT, GPIO.LOW)
    GPIO.output(IN4_LEFT, GPIO.LOW)

def move_forward():
    # print("car: Forward")
    GPIO.output(IN1_RIGHT, GPIO.HIGH)
    GPIO.output(IN2_RIGHT, GPIO.LOW)
    GPIO.output(IN3_LEFT, GPIO.HIGH)
    GPIO.output(IN4_LEFT, GPIO.LOW)

def move_left():
    # print("car: Turning Left")
    GPIO.output(IN1_RIGHT, GPIO.HIGH)
    GPIO.output(IN2_RIGHT, GPIO.LOW)
    GPIO.output(IN3_LEFT, GPIO.LOW)
    GPIO.output(IN4_LEFT, GPIO.HIGH)

def move_right():
    # print("car: Turning Right")
    GPIO.output(IN1_RIGHT, GPIO.LOW)
    GPIO.output(IN2_RIGHT, GPIO.HIGH)
    GPIO.output(IN3_LEFT, GPIO.HIGH)
    GPIO.output(IN4_LEFT, GPIO.LOW)

# --- Firefighting Functions ---
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)

def control_water_pump(on):
    global pump_on, pump_start_time
    if on and not pump_on:
        GPIO.output(PUMP_IN1, GPIO.HIGH)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        pump_on = True
        pump_start_time = time.time()
        print("Water pump ON!")
    elif not on and pump_on:
        GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        pump_on = False
        pump_start_time = 0

# --- Main Loop ---
try:
    print("Starting Raspberry Pi Auto Firefighting Robot...")
    set_servo_angle(90)
    control_water_pump(False)
    move_stop()

    while True:
        left_detected = GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW
        center_detected = GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW
        right_detected = GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW

        if left_detected and not center_detected:
            state = "TURNING_LEFT"
        elif right_detected and not center_detected:
            state = "TURNING_RIGHT"
        elif center_detected:
            state = "FORWARD"
        else:
            state = "IDLE"

        if state == "IDLE":
            print("State: IDLE. Fire not detected.")
            move_stop()
            # set_servo_angle(90)
            control_water_pump(False)
        else:
            control_water_pump(True)

            if state == "FORWARD":
                print("State: FORWARD")
                print("Center flame detected! Moving servo to 90 degrees.")
                move_forward()
                set_servo_angle(90)
            elif state == "TURNING_LEFT":
                print("State: TURNING_LEFT")
                print("Left flame detected! Moving servo to 45 degrees.")
                move_left()
                set_servo_angle(45)
            elif state == "TURNING_RIGHT":
                print("State: TURNING_RIGHT")
                print("Right flame detected! Moving servo to 135 degrees.")
                move_right()
                set_servo_angle(135)

        if pump_on and (time.time() - pump_start_time > pump_duration):
            print(f"Water pump operated for {pump_duration} seconds. Turning OFF.")
            control_water_pump(False)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    move_stop()
    control_water_pump(False)
    servo_pwm.stop()
    motor_pwm_right.stop()
    motor_pwm_left.stop()
    GPIO.cleanup()
    print("Resources cleaned up. Program exited.")