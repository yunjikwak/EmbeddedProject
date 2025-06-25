import RPi.GPIO as GPIO
import time

PUMP_IN1 = 25
PUMP_IN2 = 8

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PUMP_IN1, GPIO.OUT)
GPIO.setup(PUMP_IN2, GPIO.OUT)

# GPIO.output(PUMP_IN1, GPIO.LOW)
# GPIO.output(PUMP_IN2, GPIO.LOW)

# pump_pwm = GPIO.PWM(PUMP_IN1, 1000)
# pump_pwm.start(0)

def control_pump(on_off):
    if on_off:
        GPIO.output(PUMP_IN1, GPIO.HIGH)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("pump ON!")
    else:
        GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("pump OFF!")

def control_pump1(speed):
    # 방향 핀은 항상 LOW로 고정하여 모터가 한 방향으로만 돌도록 설정
    GPIO.output(PUMP_IN2, GPIO.LOW)

    # PWM 핀의 듀티 사이클을 조절하여 속도(수압) 제어
    pump_pwm.ChangeDutyCycle(speed)

try:
    # control_pump(70)
    # time.sleep(5)

    # control_pump(100)
    # time.sleep(10)

    # control_pump(0)
    # time.sleep(2)

    control_pump(True)
    time.sleep(2)

    control_pump(False)
    time.sleep(5)

    # while True:
    #     control_pump(True)
    #     time.sleep(5)

    #     control_pump(False)
    # time.sleep(5)

except KeyboardInterrupt:
    print("\nclose")
finally:
    # pump_pwm.stop()
    GPIO.cleanup()