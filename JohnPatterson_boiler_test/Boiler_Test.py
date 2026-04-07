import pyrebase
import time

# ----------------------------
# Firebase Configuration
# ----------------------------

firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "soupercomputer-f0dad.firebaseapp.com",
    "databaseURL": "https://soupercomputer-f0dad-default-rtdb.firebaseio.com",
    "projectId": "soupercomputer-f0dad",
    "storageBucket": "soupercomputer-f0dad.firebasestorage.app",
    "messagingSenderId": "111112419939",
    "appId": "1:111112419939:web:121ce21735c3658a185656"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# ----------------------------
# Helper Functions
# ----------------------------

def verify_exists(order_id):
    val = db.child("orders").child(order_id).get().val()

    if val:
        print(f"PASS: {order_id} exists")
    else:
        print(f"ERROR: {order_id} missing")


def verify_removed(order_id):
    val = db.child("orders").child(order_id).get().val()

    if val is None:
        print(f"PASS: {order_id} removed after completion")
    else:
        print(f"ERROR: {order_id} still exists")


def wait_for_boiler_status(expected):
    while True:
        status = db.child("boiler").child("status").child("status").get().val()

        if status == expected:
            print(f"PASS: Boiler status = {expected}")
            break

        time.sleep(1)


# ----------------------------
# Create Test Orders
# ----------------------------

print("Creating test orders...")

order1 = {
    "status": "pending",
    "time_stamp": time.time()
}

time.sleep(1)

order2 = {
    "status": "pending",
    "time_stamp": time.time()
}

db.child("orders").child("test_order_1").set(order1)
db.child("orders").child("test_order_2").set(order2)

print("Orders created")

verify_exists("test_order_1")
verify_exists("test_order_2")

# ----------------------------
# Reset Garnish
# ----------------------------

db.child("garnish").child("status").set("waiting")
print("Garnish reset")

# ============================
# TEST ORDER 1
# ============================

print("\n--- Testing Order 1 ---")

wait_for_boiler_status("heating")
wait_for_boiler_status("idle")

print("Completing garnish for order 1")
db.child("garnish").child("status").set("complete")

time.sleep(3)

verify_removed("test_order_1")

# Reset garnish for next order
db.child("garnish").child("status").set("waiting")

# ============================
# TEST ORDER 2
# ============================

print("\n--- Testing Order 2 ---")

wait_for_boiler_status("heating")
wait_for_boiler_status("idle")

print("Completing garnish for order 2")
db.child("garnish").child("status").set("complete")

time.sleep(3)

verify_removed("test_order_2")

print("\nAll tests completed.")
