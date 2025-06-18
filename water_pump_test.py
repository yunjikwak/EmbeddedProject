import RPi.GPIO as GPIO
import time

PUMP_IN1 = 17  # L9110S A-IA 
PUMP_IN2 = 18  # L9110S A-IB 

GPIO.setmode(GPIO.BCM)     
GPIO.setwarnings(False)     

GPIO.setup(PUMP_IN1, GPIO.OUT)
GPIO.setup(PUMP_IN2, GPIO.OUT)

GPIO.output(PUMP_IN1, GPIO.LOW)
GPIO.output(PUMP_IN2, GPIO.LOW)

def control_pump(on_off):
    if on_off:
        GPIO.output(PUMP_IN1, GPIO.HIGH)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("pump ON!")
    else:
        GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("pump OFF!")

try:
    while True:
        control_pump(True)
        time.sleep(5)  

        control_pump(False)
        time.sleep(5) 

except KeyboardInterrupt:
    print("\nclose")
finally:
    control_pump(False)
    GPIO.cleanup()
