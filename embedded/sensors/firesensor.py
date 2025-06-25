import RPi.GPIO as GPIO
import time

# FLAME_PIN = 12

FLAME_LEFT_PIN = 22
FLAME_CENTER_PIN = 23
FLAME_RIGHT_PIN = 24

GPIO.setmode(GPIO.BCM)
# GPIO.setup(FLAME_PIN, GPIO.IN)
GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

# def callback(FLAME_PIN) :
# 	print("flame detected")

def callback1(FLAME_LEFT_PIN) :
	print("flame left detected")
def callback2(FLAME_CENTER_PIN) :
	print("flame center detected")
def callback3(FLAME_RIGHT_PIN) :
	print("flame right detected")

# GPIO.add_event_detect(FLAME_PIN, GPIO.BOTH, bouncetime=300)
# GPIO.add_event_callback(FLAME_PIN, callback)

GPIO.add_event_detect(FLAME_LEFT_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(FLAME_LEFT_PIN, callback1)
GPIO.add_event_detect(FLAME_CENTER_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(FLAME_CENTER_PIN, callback2)
GPIO.add_event_detect(FLAME_RIGHT_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(FLAME_RIGHT_PIN, callback3)

while True:
	time.sleep(0.05)