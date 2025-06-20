import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
FLAME_LEFT_PIN = 22
FLAME_CENTER_PIN = 23
FLAME_RIGHT_PIN = 24

SERVO_PIN = 18

PUMP_IN1 = 25
PUMP_IN2 = 8

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(FLAME_LEFT_PIN, GPIO.IN)
GPIO.setup(FLAME_CENTER_PIN, GPIO.IN)
GPIO.setup(FLAME_RIGHT_PIN, GPIO.IN)

GPIO.setup(SERVO_PIN, GPIO.OUT)

GPIO.setup(PUMP_IN1, GPIO.OUT)
GPIO.setup(PUMP_IN2, GPIO.OUT)

# --- PWM Objects ---
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# --- Global Variables ---
any_flame_detected_overall = False
pump_start_time = 0
pump_duration = 5 # Pump active duration in seconds

# --- Functions ---
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)

def control_water_pump(on):
    if on:
        GPIO.output(PUMP_IN1, GPIO.HIGH)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("Water pump ON!")
    else:
        GPIO.output(PUMP_IN1, GPIO.LOW)
        GPIO.output(PUMP_IN2, GPIO.LOW)
        print("Water pump OFF!")

def flame_event_handler(channel):
    global any_flame_detected_overall
    global pump_start_time

    if GPIO.input(channel) == GPIO.LOW: # Flame detected (Active LOW)
        if not any_flame_detected_overall:
            print("\n--- NEW FIRE DETECTED ---")
            pump_start_time = time.time()

        any_flame_detected_overall = True

        if channel == FLAME_LEFT_PIN:
            print("Left flame detected! Moving servo to 45 degrees.")
            set_servo_angle(45)
        elif channel == FLAME_CENTER_PIN:
            print("Center flame detected! Moving servo to 90 degrees.")
            set_servo_angle(90)
        elif channel == FLAME_RIGHT_PIN:
            print("Right flame detected! Moving servo to 135 degrees.")
            set_servo_angle(135)
        
        control_water_pump(True)
        
    else: # Flame gone (Active HIGH)
        print(f"GPIO {channel} flame gone.")
        # Check if other flames are still detected
        if not (GPIO.input(FLAME_LEFT_PIN) == GPIO.LOW or
                GPIO.input(FLAME_CENTER_PIN) == GPIO.LOW or
                GPIO.input(FLAME_RIGHT_PIN) == GPIO.LOW):
            
            any_flame_detected_overall = False
            print("--- ALL FLAMES GONE ---")
            set_servo_angle(90)
            control_water_pump(False)

# --- Event Detection Setup ---
GPIO.add_event_detect(FLAME_LEFT_PIN, GPIO.BOTH, callback=flame_event_handler, bouncetime=300)
GPIO.add_event_detect(FLAME_CENTER_PIN, GPIO.BOTH, callback=flame_event_handler, bouncetime=300)
GPIO.add_event_detect(FLAME_RIGHT_PIN, GPIO.BOTH, callback=flame_event_handler, bouncetime=300)

# --- Main Loop ---
try:
    print("Starting Raspberry Pi auto firefighting system...")
    set_servo_angle(90)
    control_water_pump(False)

    last_print_time_no_fire = time.time()
    print_interval_no_fire = 5

    while True:
        if any_flame_detected_overall:
            if time.time() - pump_start_time > pump_duration:
                print(f"Water pump operated for {pump_duration} seconds. Turning OFF.")
                control_water_pump(False)
        else:
            if time.time() - last_print_time_no_fire > print_interval_no_fire:
                print("Fire not detected.")
                last_print_time_no_fire = time.time()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram terminated by user...")
finally:
    control_water_pump(False)
    servo_pwm.stop()
    GPIO.cleanup()
    print("Resources cleaned up. Program exited.")
