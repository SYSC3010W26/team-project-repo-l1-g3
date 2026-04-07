import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO # Added GPIO library

# --- CONFIGURATION ---
DATABASE_URL = "https://soupercomputer-f0dad-default-rtdb.firebaseio.com/"

# --- HARDWARE PIN CONFIGURATION ---
TRIGGER_PIN = 4
ECHO_PIN = 17
SERVO_PIN = 18

# --- FIREBASE SETUP ---
if not firebase_admin._apps:
    cred = credentials.Certificate("soupercomputer-f0dad-firebase-adminsdk-fbsvc-9d52dc6494.json")
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

# --- HARDWARE INITIALIZATION ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Setup Servo
servo = GPIO.PWM(SERVO_PIN, 50) # 50Hz PWM
servo.start(0)

# --- HARDWARE FUNCTIONS ---
def check_ultrasonic_sensor():
    """Reads actual distance from the physical HC-SR04 sensor."""
    # Send 10 microsecond pulse
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start_time = time.time()
    stop_time = time.time()
    
    # Timeout protection (prevents freezing if a wire is loose)
    timeout_start = time.time()

    # Wait for Echo to go HIGH
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
        if time.time() - timeout_start > 0.1: 
            break

    # Wait for Echo to go LOW
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
        if time.time() - timeout_start > 0.1:
            break

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    
    print(f"[HARDWARE] Ultrasonic Sensor read: {distance:.1f}cm")
    return distance

def activate_servo():
    """Moves the physical SG90 servo."""
    print("    [HARDWARE ACTUATION] >> Servo: 90 DEG (OPEN)")
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(7) # 90 degrees
    time.sleep(1)
    
    print("    [HARDWARE ACTUATION] >> Servo: 0 DEG (CLOSED)")
    servo.ChangeDutyCycle(2) # 0 degrees
    time.sleep(1)
    
    # Stop sending signal to prevent servo jitter
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# --- MAIN LOGIC ---
def garnish_logic_loop():
    print("--- GARNISH NODE HARDWARE RUNNING ---")
    print("Waiting for Firebase updates...")
    
    # Reset status to idle at start
    db.reference('/garnish/status').set("idle")

    try:
        while True:
            # 1. CHECK MIXER STATUS
            mixer_data = db.reference('/mixer/status').get()
            
            if isinstance(mixer_data, dict):
                current_mixer_status = mixer_data.get('status')
            else:
                current_mixer_status = mixer_data

            my_status = db.reference('/garnish/status').get()
            
            # 2. TRIGGER LOGIC
            if current_mixer_status == "complete" and my_status == "idle":
                print("\n[EVENT] Mixer finished. Processing Order...")

                order_data = db.reference('/orders/current_order').get()
                
                if order_data:
                    toppings_list = order_data.get('toppings',[])
                    
                    if toppings_list and len(toppings_list) > 0 and toppings_list != [""]:
                        print(f"[LOGIC] Toppings found: {toppings_list}")
                        
                        # 3. READ PHYSICAL BOWL SENSOR
                        distance = check_ultrasonic_sensor()
                        
                        if distance < 10.0:
                            # HAPPY PATH
                            print("[ACTION] Bowl detected! Dispensing...")
                            db.reference('/garnish/status').set("dispensing")
                            
                            # MOVE PHYSICAL SERVO
                            activate_servo()
                            
                            print("[ACTION] Done.")
                            db.reference('/garnish/status').set("complete")
                        else:
                            # ERROR PATH
                            print("[ERROR] No Bowl detected!")
                            db.reference('/garnish/status').set("error")
                    else:
                        print("[LOGIC] No toppings required.")
                        db.reference('/garnish/status').set("complete")
                
            time.sleep(1) # Poll frequency

    except KeyboardInterrupt:
        print("\nShutting down Hardware Node...")
    finally:
        # CLEANUP (Includes the fix we discovered earlier!)
        servo.stop()
        del servo 
        GPIO.cleanup()

if __name__ == "__main__":
    garnish_logic_loop()
