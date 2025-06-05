import RPi.GPIO as GPIO
import time

FLAME_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

def callback(FLAME_PIN) :
	print("flame detected")

GPIO.add_event_detect(FLAME_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(FLAME_PIN, callback)

while True:
	time.sleep(1)
