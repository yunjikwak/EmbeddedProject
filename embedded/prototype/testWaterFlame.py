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
pump_duration = 2 # Pump active duration in seconds
state = "IDLE"
last_state = "IDLE"
movement_start_time = 0
movement_duration = 3

# --- rccar Control Functions ---
def set_speed_straight():
    motor_pwm_right.ChangeDutyCycle(75)
    motor_pwm_left.ChangeDutyCycle(75)

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
    GPIO.output(IN4_LEFT, GPIO.HIGH)
    GPIO.output(IN3_LEFT, GPIO.LOW)
    # time.sleep(5)
    # move_stop()

def curve_left():
    GPIO.output(IN1_RIGHT, GPIO.HIGH)
    GPIO.output(IN2_RIGHT, GPIO.LOW)
    GPIO.output(IN4_LEFT, GPIO.HIGH)
    GPIO.output(IN3_LEFT, GPIO.LOW)
    motor_pwm_right.ChangeDutyCycle(95) #fast
    motor_pwm_left.ChangeDutyCycle(30) #slow
    # time.sleep(1)
    # move_stop()

def curve_right():
    GPIO.output(IN1_RIGHT, GPIO.HIGH)
    GPIO.output(IN2_RIGHT, GPIO.LOW)
    GPIO.output(IN4_LEFT, GPIO.HIGH)
    GPIO.output(IN3_LEFT, GPIO.LOW)
    motor_pwm_right.ChangeDutyCycle(25)  # slow
    motor_pwm_left.ChangeDutyCycle(100)
    # time.sleep(1)
    # move_stop()

# --- Firefighting Functions ---
def set_servo_angle(angle):
    print("set")
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    # time.sleep(0.1)

def control_water_pump(on):
    global pump_on, pump_start_time
    if on and not pump_on:
        GPIO.output(PUMP_IN1, GPIO.HIGH)
        # GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        pump_on = True
        pump_start_time = time.time()
        print("Water pump ON!")
    elif not on:
        GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        pump_on = False
        pump_start_time = 0
        print("Water pump OFF!")
    # elif not on and pump_on:
    #     GPIO.output(PUMP_IN1, GPIO.LOW)
    #     GPIO.output(PUMP_IN2, GPIO.LOW)
    #     pump_on = False
    #     pump_start_time = 0
    #     print("Water pump OFF!")

# --- Main Loop ---
try:
    set_servo_angle(90)
    control_water_pump(False)
    move_stop()

    while True:
        left_detected = GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW
        center_detected = GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW
        right_detected = GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW

        # user_input = input("Enter sensor state (L C R) as 3 digits (e.g., 100, 010, 000) or 'exit': ")

        # if user_input.lower() == 'exit':
        #         break # 루프 탈출

        # if len(user_input) == 3 and all(c in '01' for c in user_input):
        #     left_detected = (user_input[0] == '1')
        #     center_detected = (user_input[1] == '1')
        #     right_detected  = (user_input[2] == '1')
        #     print(f"Simulating: Left={left_detected}, Center={center_detected}, Right={right_detected}")
        # else:
        #     print("Invalid input. Please enter 3 digits (0 or 1).")
        #     continue

        desired_state = "IDLE"
        if center_detected:
            desired_state = "FORWARD"
        elif right_detected:
            desired_state = "TURNING_RIGHT"
        elif left_detected:
            desired_state = "TURNING_LEFT"

        is_seeking = state not in ["IDLE", "ATTACKING"]

        next_state = state

        if is_seeking:
            if time.time() - movement_start_time > movement_duration:
                next_state = "ATTACKING" # 움직임 시간 초과 -> 공격
            elif desired_state == "IDLE":
                next_state = "IDLE" # 움직이다 목표 사라짐 -> 대기
        elif state == "ATTACKING":
            is_pump_time_over = pump_on and (time.time() - pump_start_time > pump_duration)
            if is_pump_time_over or desired_state == "IDLE":
                next_state = "IDLE" # 펌프 시간 초과 or 목표 사라짐 -> 대기
        elif state == "IDLE" and desired_state != "IDLE":
             # IDLE 상태에서 불꽃을 발견하면, 구체적인 방향이 아닌 '탐색' 상태로 전환
             next_state = "SEEKING"
        # # complete move -> attack
        # if is_seeking and time.time() - movement_start_time > movement_duration:
        #     next_state = "ATTACKING"
        #     # movement_start_time = 0
        # # pump time over or fire gone -> idle
        # elif is_seeking and desired_state != state:
        #     next_state = "IDLE"
        # elif state == "ATTACKING" and (desired_state == "IDLE" or (pump_on and time.time() - pump_start_time > pump_duration)):
        #     next_state = "IDLE"
        # elif state == "IDLE" and desired_state != "IDLE":
        #     next_state = desired_state

        state = next_state

        if state != last_state:
            # print(f"\n--- State changed: {last_state} -> {state} (Desired Direction: {desired_state}) ---")

            # 상태가 SEEKING으로 바뀌는 순간, 움직임 타이머 시작
            if state == "SEEKING":
                movement_start_time = time.time()
            # 상태가 IDLE로 바뀌는 순간, 서보를 중앙으로
            # elif state == "IDLE":
            #     set_servo_angle(90)
            # 상태가 ATTACKING으로 바뀌는 순간, 마지막 탐색 방향으로 최종 조준
            elif state == "ATTACKING":
                print("Target acquired. Aiming servo...", desired_state)
                if desired_state == "FORWARD":
                    set_servo_angle(90)
                elif desired_state == "TURNING_LEFT":
                    set_servo_angle(145)
                elif desired_state == "TURNING_RIGHT":
                    set_servo_angle(35)

        # # for servo
        # if state != last_state:
        #     if state == "ATTACKING":
        #         print("Attcking")
        #         if last_state == "FORWARD" or last_state == "IDLE":
        #             set_servo_angle(90)
        #         elif last_state == "TURNING_LEFT":
        #             set_servo_angle(145)
        #         elif last_state == "TURNING_RIGHT":
        #             set_servo_angle(35)

        #     if state == "SEEKING":
        #         movement_start_time = time.time()

        #     # if state not in ["IDLE", "ATTACKING"]: # 탐색 상태로 진입 시
        #     #     movement_start_time = time.time()
        last_state = state

        if state == "IDLE":
            print("State: IDLE. Fire not detected. water stop")
            move_stop()
            control_water_pump(False)
        elif state == "ATTACKING":
            move_stop()
            control_water_pump(True)
        else: # moving
            control_water_pump(False)

            if desired_state == "FORWARD":
                print("State: FORWARD")
                set_speed_straight()
                move_forward()
            elif desired_state == "TURNING_LEFT":
                print("State: TURNING_LEFT")
                curve_left()
            elif desired_state == "TURNING_RIGHT":
                print("State: TURNING_RIGHT")
                curve_right()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    move_stop()
    control_water_pump(False)
    servo_pwm.stop()
    motor_pwm_right.stop()
    motor_pwm_left.stop()
    GPIO.cleanup()