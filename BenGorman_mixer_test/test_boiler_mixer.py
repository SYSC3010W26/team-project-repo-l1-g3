import pyrebase
import time

# Use your existing firebaseConfig here
firebaseConfig = {
    "apiKey": "AIzaSyAC0Ln-uwvVyqcfXWOO52_uFt-q_KuVr9A",
    "authDomain": "soupercomputer-f0dad.firebaseapp.com",
    "databaseURL": "https://soupercomputer-f0dad-default-rtdb.firebaseio.com",
    "projectId": "soupercomputer-f0dad",
    "storageBucket": "soupercomputer-f0dad.firebasestorage.app",
    "messagingSenderId": "111112419939",
    "appId": "1:111112419939:web:121ce21735c3658a185656"} 

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def verify_status(expected_mixer_status):
    current_data = db.child("mixer").child("status").get().val()
    actual_status = current_data.get("status") if current_data else None
    
    if actual_status == expected_mixer_status:
        print(f"TEST PASSED: Mixer is '{actual_status}'")
        return True
    else:
        print(f"TEST FAILED: Expected '{expected_mixer_status}', but found '{actual_status}'")
        return False

def run_tests():
    print("--- Starting Automated Logic Tests ---")

    # TEST CASE 1: The Error Case
    print("\n[TEST 1] Testing 'Unexpected Status'...")
    db.child("boiler").child("status").set("malfunction")
    time.sleep(2) # Wait for listener to react
    # Verification: Mixer should still be 'waiting' because 'malfunction' shouldn't trigger it
    verify_status("waiting")

    # TEST CASE 2: The Success Case
    print("\n[TEST 2] Testing 'Success' Trigger...")
    db.child("boiler").child("status").set("complete")
    
    # Wait 3 seconds to ensure it has started mixing (20% mark)
    time.sleep(3)
    verify_status("mixing")
    
    # Wait for the full cycle to finish (10s + buffer)
    print("Waiting for cycle completion...")
    time.sleep(10)
    
    # Verification: Mixer should have finished and returned to 'waiting'
    verify_status("waiting")

if __name__ == "__main__":
    run_tests()
