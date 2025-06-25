import RPi.GPIO as GPIO
import time

# FLAME_PIN = 12
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(FLAME_PIN, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# watorservo = GPIO.PWM(WATORSERVO, 1000)
# watorservo.start(0)

def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

def move_left():
    set_servo_angle(145)

def move_right():
    set_servo_angle(35)

# def fire_detected(FLAME_PIN) :
# 	for i in range(91) : #check left
# 		watorservo.ChangeDutyCycle(i)
# 		time.sleep(0.01)
# 	print("Left flame detected")
# 	time.sleep(3)

# GPIO.add_event_detect(FLAME_PIN, GPIO.BOTH, callback = fire_detected, bouncetime=300)

# try :
# 	while True:
# 		for i in range(91) : #check left
# 			watorservo.ChangeDutyCycle(i)
# 			time.sleep(0.01)
# 		print("Left flame detected")
# 		time.sleep(3)
# 		time.sleep(1)
# except KeyboardInterrupt:
# 	GPIO.cleanup()

try:
    set_servo_angle(90) #front
    set_servo_angle(35) #right
    set_servo_angle(145) #right
except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    # 프로그램 종료 시 안전하게 리소스 정리
    print("Cleaning up GPIO...")
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")