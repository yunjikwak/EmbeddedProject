import RPi.GPIO as GPIO
import time # Time library for delays

STOP = 0        
FORWARD = 1     
BACKWARD = 2

CH1 = 0 # First motor channel 
CH2 = 1 # Second motor channel 

ENA = 26 # GPIO 12
ENB = 19 # GPIO 13 

IN1 = 24 
IN2 = 23 
IN3 = 5 
IN4 = 6 

GPIO.setmode(GPIO.BCM)      
#GPIO.setwarnings(False)

def setup_motor_pins(EN_PIN, INA_PIN, INB_PIN):
    GPIO.setup(EN_PIN, GPIO.OUT)  
    GPIO.setup(INA_PIN, GPIO.OUT) 
    GPIO.setup(INB_PIN, GPIO.OUT) 
    
    pwm_obj = GPIO.PWM(EN_PIN, 100)
    pwm_obj.start(0) 
    return pwm_obj 

def set_motor_control(pwm_obj, INA_PIN, INB_PIN, speed, stat):
    pwm_obj.ChangeDutyCycle(speed)

    if stat == FORWARD: # Move forward
        GPIO.output(INA_PIN, GPIO.HIGH)
        GPIO.output(INB_PIN, GPIO.LOW)
    elif stat == BACKWARD: # Move backward
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.HIGH)
    elif stat == STOP: # Stop motor
        GPIO.output(INA_PIN, GPIO.LOW)
        GPIO.output(INB_PIN, GPIO.LOW)

        pwm_obj.ChangeDutyCycle(0)

def set_motor(ch, speed, stat):
    if ch == CH1: # Control the first motor
        set_motor_control(pwm_ch1, IN1, IN2, speed, stat)
    else: # Control the second motor
        set_motor_control(pwm_ch2, IN3, IN4, speed, stat)

# --- Main Code Execution ---
pwm_ch1 = setup_motor_pins(ENA, IN1, IN2)
pwm_ch2 = setup_motor_pins(ENB, IN3, IN4)

print("Starting motor control...")

try:
    set_motor(CH1, 70, FORWARD) 
    set_motor(CH2, 70, FORWARD)
    print("Moving forward for 5 seconds (speed 70%)")
    time.sleep(5) 

    set_motor(CH1, 40, BACKWARD) 
    set_motor(CH2, 40, BACKWARD)
    print("Moving backward for 5 seconds (speed 40%)")
    time.sleep(5)

    set_motor(CH1, 100, BACKWARD) 
    set_motor(CH2, 100, BACKWARD)
    print("Moving backward for 5 seconds (speed 100%)")
    time.sleep(5)

    set_motor(CH1, 0, STOP) # Set speed to 0 for stop
    set_motor(CH2, 0, STOP)
    print("Motors stopped")
    time.sleep(1) 

except KeyboardInterrupt:
    print("\nProgram termination requested by user...")

finally:
    # --- Cleanup on Exit ---
    print("Cleaning up resources...")
    # Ensure all motors are stopped
    set_motor(CH1, 0, STOP)
    set_motor(CH2, 0, STOP)
    
    pwm_ch1.stop
    pwm_ch2.stop
    GPIO.cleanup()
