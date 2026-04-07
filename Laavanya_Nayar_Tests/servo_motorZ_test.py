import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50) # 50Hz
servo.start(0)

print("--- HARDWARE TEST: SERVO MOTOR ---")
try:
    print("Moving to 90 degrees (Open)...")
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(7)
    time.sleep(1)
    
    print("Moving to 0 degrees (Closed)...")
    servo.ChangeDutyCycle(2)
    time.sleep(1)
    
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)
    print("Test passed.")

finally:
    servo.stop()
    del servo       # <--- THE FIX: Destroys the PWM object first
    GPIO.cleanup()  # Then safely cleans up the pins
