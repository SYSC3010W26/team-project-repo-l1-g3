import pyrebase
import time
from datetime import datetime

# ---------------------------------
# Firebase Configuration
# ---------------------------------
firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
	"authDomain": "soupercomputer-f0dad.firebaseapp.com",
	"databaseURL": "https://soupercomputer-f0dad-default-rtdb.firebaseio.com",
	"projectId": "soupercomputer-f0dad",
	"storageBucket": "soupercomputer-f0dad.firebasestorage.app",
	"messagingSenderId": "111112419939",
	"appId": "1:111112419939:web:121ce21735c3658a185656"
}

MIX_TIME = 10
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# ---------------------------------
# Helper Function
# ---------------------------------

def write_mixer_status(status_string, progress=0):
    mixer_data = {
        "progress": progress,
        "status": status_string,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    # Writes to /mixer/status
    db.child("mixer").child("status").set(mixer_data)
    print(f"Mixer updated: {status_string} ({progress}%)")#
    
def add_ingredient():
    print(">>> [ACTION] Adding ingredient at 20% mark...")
    # You could also update a 'dispenser' status in Firebase here
    db.child("mixer").child("logs").push({
        "event": "ingredient_added",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

# ---------------------------------
# Listener Callbacks
# ---------------------------------

def mix_order():
    print("Sequence Triggered: Mixing...")
    
    # Start mixing
    for i in range(MIX_TIME + 1):
        percent = int((i / MIX_TIME) * 100)
        write_mixer_status("mixing", progress=percent)
        if percent == 20:
            add_ingredient()
        time.sleep(1)
    
    # Finalize
    write_mixer_status("complete", progress=100)
    print("Mixing sequence finished.")
    
    # Reset to waiting for next boiler cycle
    write_mixer_status("waiting", progress=0)

def boiler_listener(message):
    new_status = message.get("data")
    
    # CASE 1: Success/Ready Trigger
    if new_status == "complete" or new_status == "idle":
        print(f"Boiler Status: {new_status}. Triggering Mixer...")
        mix_order()
    
    # CASE 2: Normal intermediate states (Optional but keeps console clean)
    elif new_status == "heating" or new_status == "waiting":
        print(f"Boiler is busy: {new_status}. Mixer standing by...")

    # CASE 3: The Error Case
    else:
        print(f"Error: Unexpected status of boiler -> '{new_status}'")

# ---------------------------------
# Main Execution
# ---------------------------------

if __name__ == "__main__":
    print("Setting initial Mixer state...")
    write_mixer_status("waiting")

    print("Starting Listener on /boiler/status...")
    # .stream() starts a background thread automatically
    boiler_stream = db.child("boiler").child("status").stream(boiler_listener)

    try:
        # Keep the main thread alive so the listener doesn't close
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        boiler_stream.close()
