import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# --- CONFIGURATION ---
# REPLACE WITH YOUR GROUP'S URL

DATABASE_URL = "https://soupercomputer-f0dad-default-rtdb.firebaseio.com/"

# --- FIREBASE SETUP ---
# Only initialize if not already initialized (prevents errors if imported)
if not firebase_admin._apps:
    cred = credentials.Certificate("soupercomputer-f0dad-firebase-adminsdk-fbsvc-9d52dc6494.json")
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

# --- HARDWARE STUBS (Controlled by DB for Testing) ---
def check_ultrasonic_sensor():
    """
    Reads from a simulation path in DB to decide if a bowl is present.
    This allows the Test Script to 'remove the bowl' remotely.
    """
    try:
        # Default to 5cm (Bowl Present) if simulation value is missing
        sim_dist = db.reference('/sim_hardware/distance').get()
        if sim_dist is None: 
            return 5.0
        return float(sim_dist)
    except Exception as e:
        print(f"[HW-SIM] Error reading sim distance: {e}")
        return 5.0

def activate_servo():
    """Simulates the servo moving."""
    print("    [HARDWARE ACTUATION] >> Servo: 90 DEG (OPEN)")
    time.sleep(1)
    print("    [HARDWARE ACTUATION] >> Servo: 0 DEG (CLOSED)")

# --- MAIN LOGIC ---
def garnish_logic_loop():
    print("--- GARNISH NODE SIMULATION RUNNING ---")
    print("Waiting for Firebase updates...")
    
    # Reset status to idle at start
    db.reference('/garnish/status').set("idle")

    while True:
        try:
            # 1. CHECK MIXER STATUS
            mixer_data = db.reference('/mixer/status').get()
            
            # Handle dictionary vs string return from Firebase
            if isinstance(mixer_data, dict):
                current_mixer_status = mixer_data.get('status')
            else:
                current_mixer_status = mixer_data

            # ONLY ACT if mixer is complete AND we haven't already finished
            # (Checks if we are currently idle to prevent double dispensing)
            my_status = db.reference('/garnish/status').get()
            
            if current_mixer_status == "complete" and my_status == "idle":
                print("\n[EVENT] Mixer finished. Processing Order...")

                # 2. CHECK ORDER
                order_data = db.reference('/orders/1').get()
                
                if order_data:
                    toppings_list = order_data.get('toppings', [])
                    
                    # LOGIC: Check for toppings
                    # Handle cases where toppings might be None or Empty list
                    if toppings_list and len(toppings_list) > 0 and toppings_list != [""]:
                        print(f"[LOGIC] Toppings found: {toppings_list}")
                        
                        # 3. CHECK BOWL SENSOR
                        distance = check_ultrasonic_sensor()
                        print(f"[SENSOR] Distance read: {distance}cm")
                        
                        if distance < 10:
                            # HAPPY PATH
                            print("[ACTION] Dispensing...")
                            db.reference('/garnish/status').set("dispensing")
                            activate_servo()
                            
                            print("[ACTION] Done.")
                            db.reference('/garnish/status').set("complete")
                        else:
                            # SAFETY ERROR
                            print("[ERROR] No Bowl detected!")
                            db.reference('/garnish/status').set("error")
                    else:
                        print("[LOGIC] No toppings required.")
                        db.reference('/garnish/status').set("complete")
                
            time.sleep(1) # Poll frequency

        except KeyboardInterrupt:
            print("\nSimulation Stopped.")
            break
        except Exception as e:
            print(f"Error in loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    garnish_logic_loop()
