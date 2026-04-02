import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from sense_hat import SenseHat

print("\n[SYSTEM] Initializing SouperComputer Mixer Node...")

# --- HARDWARE CONFIGURATION ---
# IBT-2 BTS7960 H-Bridge motor driver
# PINOUT:
# RPWM: GPIO 18 (Physical Pin 12) - Forward PWM
# LPWM: GPIO 19 (Physical Pin 35) - Backward PWM
# R_EN: GPIO 23 (Physical Pin 16) - Right/Forward enable
# L_EN: GPIO 24 (Physical Pin 18) - Left/Backward enable

try:
    motor_rpwm = PWMOutputDevice(18, frequency=300)
    motor_lpwm = PWMOutputDevice(19, frequency=300)
    motor_r_en = DigitalOutputDevice(23)
    motor_l_en = DigitalOutputDevice(24)
    sense = SenseHat()
    sense.clear()
except Exception as e:
    print(f"[FATAL ERROR] Hardware setup failed: {e}")
    exit(1)

# --- MIXER CONFIGURATION ---
MIX_DURATION_SECONDS = 10.0   # How long to run the mixer (tune this)
MOTOR_SPEED = 0.8              # PWM duty cycle 0.0 - 1.0 (tune this)

# --- FIREBASE SETUP ---
DATABASE_URL = "https://soupercomputer-group-l1g3-default-rtdb.firebaseio.com/"
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

# --- HELPER FUNCTIONS ---
def motor_forward(speed):
    """Spin motor forward at given speed (0.0 - 1.0)."""
    motor_r_en.on()
    motor_l_en.off()
    motor_rpwm.value = speed
    motor_lpwm.value = 0.0

def motor_stop():
    """Hard stop the motor."""
    motor_rpwm.value = 0.0
    motor_lpwm.value = 0.0
    motor_r_en.off()
    motor_l_en.off()

def run_mixer():
    """
    Mixing Sequence:
    1. Start motor at configured speed.
    2. Run for MIX_DURATION_SECONDS.
    3. Stop motor and signal complete.
    """
    print(f"[ACTION] Starting mixer for {MIX_DURATION_SECONDS}s at speed {MOTOR_SPEED}...")

    motor_forward(MOTOR_SPEED/3)
    time.sleep(MIX_DURATION_SECONDS/3)
    motor_forward(2*MOTOR_SPEED/3)
    time.sleep(MIX_DURATION_SECONDS/3)
    motor_forward(MOTOR_SPEED)
    time.sleep(MIX_DURATION_SECONDS/3)
    motor_stop()

    print("[ACTION] Mixing complete. Motor stopped.")

def spin_360_servo(servo_obj, direction, duration):
    """Spins a continuous rotation servo using gpiozero PWM."""
    if duration <= 0: return
    
    # 0.10 (10%) = Forward, 0.05 (5%) = Backward
    duty_cycle = 0.10 if direction == "fwd" else 0.05
    
    servo_obj.value = duty_cycle
    time.sleep(duration)
    servo_obj.value = 0.0 # Hard stop
    time.sleep(0.2) # Let momentum settle
def dispense_toppings(toppings_list):
    """
    Mechanical Sequence:
    1. Spin indexer FWD to the topping station.
    2. Open hopper door -> Wait -> Close hopper door.
    3. Spin indexer BWD to the Exit Station (0 degrees) to drop into soup.
    """
    print("[ACTION] Starting Dispense Sequence...")
    sense.show_letter("D", text_colour=[0, 0, 255]) 
    
    for topping in toppings_list:
        topping_key = str(topping).lower() 
        
        if topping_key in TRAVEL_TIMES_FORWARD:
            time_fwd = TRAVEL_TIMES_FORWARD[topping_key]
            time_bwd = TRAVEL_TIMES_BACKWARD[topping_key]
            
            print(f"  -> Moving indexer to {topping} ({time_fwd}s)")
            # 1. Move Indexer to Station
            spin_360_servo(indexer_servo, "fwd", time_fwd)
            
            # 2. Open Door to drop topping INTO the indexer hole
            print(f"  -> Opening hopper door...")
            spin_360_servo(door_servo, "fwd", 0.3) # 0.3s open time (TUNE THIS)
            time.sleep(0.5) # Wait for ingredients to fall
            
            # 3. Close Door
            print(f"  -> Closing hopper door...")
            spin_360_servo(door_servo, "bwd", 0.3) # 0.3s close time (TUNE THIS)
            
            # 4. Return Indexer to Exit Station to drop into soup
            print(f"  -> Returning indexer to Exit Drop ({time_bwd}s)")
            spin_360_servo(indexer_servo, "bwd", time_bwd)
            time.sleep(0.5) # Let it fall into the bowl
            
        else:
            print(f"  [WARNING] Kiosk asked for unknown base: '{soup_type}'.")

    print("[ACTION] Dispense Sequence Complete.")

# --- MAIN LOOP ---
def main():
    print("--- MIXER NODE READY ---")
    print("[INFO] Waiting for boiler_node 'ready' signal at /boiler/status")

    # Reset node status on boot
    db.reference('/mixer/status').set("idle")

    try:
        while True:
            boiler_status  = db.reference('/boiler/status').get()
            my_status      = db.reference('/mixer/status').get()
            current_order  = db.reference('/orders/1').get()

            # Auto-Reset Logic
            if not current_order and my_status != "idle":
                print("[SYSTEM] Order queue empty. Resetting to IDLE.")
                db.reference('/mixer/status').set("idle")
                sense.clear()
                time.sleep(1)
                continue

            # Processing Logic
            if current_order and boiler_status == "ready" and my_status == "idle":
                print("\n[EVENT] Boiler ready. Starting mixing sequence...")

                db.reference('/mixer/status').set("mixing")
                sense.show_letter("M", text_colour=[0, 0, 255])

                run_mixer()

                print("[SUCCESS] Mixing done. Signalling garnish node.")
                db.reference('/mixer/status').set("complete")
                sense.show_letter("C", text_colour=[0, 255, 0])

            time.sleep(0.2)  # Fast polling for responsiveness

    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down Mixer Node...")
    finally:
        motor_stop()
        sense.clear()

if __name__ == "__main__":
    main()
