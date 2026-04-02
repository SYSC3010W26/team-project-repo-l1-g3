import RPi.GPIO as GPIO
import time

# --- CONFIGURATION ---
INDEXER_SERVO_PIN = 18  # Change if you put the indexer on a different pin

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(INDEXER_SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(INDEXER_SERVO_PIN, 50) # 50Hz
servo.start(0)

print("\n--- FT90R 360 SERVO CALIBRATION TOOL ---")
print("We will test how far the servo spins based on the time you enter.")
print("Press Ctrl+C to quit.\n")

try:
    while True:
        # Get user input
        spin_time = input("Enter time to spin FORWARD in seconds (e.g., 0.5): ")
        spin_time = float(spin_time)
        
        print(f"Spinning FORWARD for {spin_time} seconds...")
        # 10.0 Duty Cycle = Spin Forward (Counter-Clockwise usually)
        GPIO.output(INDEXER_SERVO_PIN, True)
        servo.ChangeDutyCycle(10.0) 
        time.sleep(spin_time)
        
        # STOP
        servo.ChangeDutyCycle(0)
        GPIO.output(INDEXER_SERVO_PIN, False)
        
        print("STOPPED. Look at your 3D print. Did it line up perfectly?")
        
        # Test the return journey
        input("\nPress ENTER to spin BACKWARD to the start position...")
        print(f"Spinning BACKWARD for {spin_time} seconds...")
        
        # 5.0 Duty Cycle = Spin Backward (Clockwise usually)
        GPIO.output(INDEXER_SERVO_PIN, True)
        servo.ChangeDutyCycle(5.0)
        time.sleep(spin_time)
        
        # STOP
        servo.ChangeDutyCycle(0)
        GPIO.output(INDEXER_SERVO_PIN, False)
        
        print("\n" + "="*40 + "\n")

except KeyboardInterrupt:
    print("\nCalibration ended.")
finally:
    servo.stop()
    GPIO.cleanup()