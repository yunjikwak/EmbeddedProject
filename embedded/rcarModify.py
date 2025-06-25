import RPi.GPIO as GPIO

import time


GPIO.setwarnings(False)

# --- Pin Definitions (기존과 동일) ---
# Right Motor
in1 = 17
in2 = 27
en_a = 12
# Left Motor
in3 = 5
in4 = 6
en_b = 13


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en_b,GPIO.OUT)

# PWM 객체 (q: 오른쪽 바퀴 속도, p: 왼쪽 바퀴 속도)
q=GPIO.PWM(en_a,100)
p=GPIO.PWM(en_b,100)
p.start(75)
q.start(75)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)

def move_stop():
    # print("Stop")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)

try:
    # 무한 루프로 사용자 입력 대기
    while(True):
        user_input = input("w: forward, s: backward, a: left, d: right, c: stop >> ")

        if user_input == 'w':
            # 직진 또는 후진 시에는 양쪽 바퀴 속도를 동일하게 설정
            p.ChangeDutyCycle(75)
            q.ChangeDutyCycle(75)

            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            # time.sleep(15)
            # move_stop()
            print("Forward")

        elif user_input == 's':
            # 직진 또는 후진 시에는 양쪽 바퀴 속도를 동일하게 설정
            p.ChangeDutyCycle(75)
            q.ChangeDutyCycle(75)

            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            print('Back')

        # --- 오른쪽 곡선 회전으로 수정 ---
        elif user_input == 'd':
            print('Curving Right')
            q.ChangeDutyCycle(25)  # 오른쪽 바퀴(안쪽) 속도 저하
            p.ChangeDutyCycle(100)  # 왼쪽 바퀴(바깥쪽) 속도 증가
            # 1. 양쪽 바퀴 모두 전진 방향으로 설정
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            # 2. 바퀴 속도 조절로 곡선 회전 구현 (안쪽 바퀴를 느리게, 바깥쪽 바퀴를 빠르게)

        # --- 왼쪽 곡선 회전으로 수정 ---
        elif user_input == 'a':
            print('Curving Left')
            # 1. 양쪽 바퀴 모두 전진 방향으로 설정
            q.ChangeDutyCycle(95)  # 오른쪽 바퀴(바깥쪽) 속도 증가
            p.ChangeDutyCycle(30)  # 왼쪽 바퀴(안쪽) 속도 저하
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            # 2. 바퀴 속도 조절로 곡선 회전 구현 (안쪽 바퀴를 느리게, 바깥쪽 바퀴를 빠르게)

        elif user_input == 'c':
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            print('Stop')

except KeyboardInterrupt:
    # Ctrl+C 입력 시 GPIO 설정 초기화
    GPIO.cleanup()
    print("GPIO Clean up")