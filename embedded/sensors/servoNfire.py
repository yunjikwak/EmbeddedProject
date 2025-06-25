import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

FLAME_LEFT_PIN = 22
FLAME_CENTER_PIN = 23
FLAME_RIGHT_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

def move_center():
    set_servo_angle(90)

def move_left():
    set_servo_angle(145)

def move_right():
    set_servo_angle(35)

try:
    state = "IDLE"
    last_state = "IDLE"

    move_center()

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

        if state != last_state:
            if state == "FORWARD":
                move_center()
            elif state == "TURNING_LEFT":
                move_left()
            elif state == "TURNING_RIGHT":
                move_right()
            elif state == "IDLE":
                # IDLE 상태로 돌아올 때 중앙으로 복귀
                move_center()

        last_state = state
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    # 프로그램 종료 시 안전하게 리소스 정리
    print("Cleaning up GPIO...")
    move_center()
    time.sleep(0.5)
    servo_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")