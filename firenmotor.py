import RPi.GPIO as GPIO
import time

FLAME_PIN = 12
WATORSERVO = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)
GPIO.setup(WATORSERVO, GPIO.OUT)

watorservo = GPIO.PWM(WATORSERVO, 1000)
watorservo.start(0)

def fire_detected(FLAME_PIN) :
	for i in range(91) : #check left 
		watorservo.ChangeDutyCycle(i)
		time.sleep(0.01)
	print("Left flame detected")
	time.sleep(3)
	

GPIO.add_event_detect(FLAME_PIN, GPIO.BOTH, callback = fire_detected, bouncetime=300)

try :
	while True:
		for i in range(91) : #check left 
			watorservo.ChangeDutyCycle(i)
			time.sleep(0.01)
		print("Left flame detected")
		time.sleep(3)
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
