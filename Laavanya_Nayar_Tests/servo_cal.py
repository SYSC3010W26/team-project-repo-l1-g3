import RPi.GPIO as GPIO
import time

# --- CONFIGURATION ---
INDEXER_SERVO_PIN = 18  # Change if you put the indexer on a different pin

# --- FORCE CLEANUP PREVIOUS CRASHES ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
try:
    GPIO.cleanup(INDEXER_SERVO_PIN)
except:
    pass

# Setup
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
        try:
            spin_time = float(spin_time)
        except ValueError:
            print("Please enter a valid number.")
            continue

        print(f"Spinning FORWARD for {spin_time} seconds...")
        # 10.0 Duty Cycle = Spin Forward
        GPIO.output(INDEXER_SERVO_PIN, True)
        servo.ChangeDutyCycle(10.0)
        time.sleep(spin_time)

        # HARD STOP
        servo.ChangeDutyCycle(0)
        GPIO.output(INDEXER_SERVO_PIN, False)

        print("STOPPED. Look at your 3D print. Did it line up perfectly?")

        # Test the return journey
        input("\nPress ENTER to spin BACKWARD to the start position...")
        print(f"Spinning BACKWARD for {spin_time} seconds...")

        # 5.0 Duty Cycle = Spin Backward
        GPIO.output(INDEXER_SERVO_PIN, True)
        servo.ChangeDutyCycle(5.0)
        time.sleep(spin_time)

        # HARD STOP
        servo.ChangeDutyCycle(0)
        GPIO.output(INDEXER_SERVO_PIN, False)
        print("\n------------------------------------------------")

except KeyboardInterrupt:
    print("\nCalibration stopped by user. Cleaning up...")

finally:
    # CRITICAL FIX: This releases the pin so you don't get the error next time!
    print("Releasing GPIO Pin 18...")
    servo.stop()
    GPIO.cleanup()