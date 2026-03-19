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
db.child("orders").remove()

# ----------------------------
# Boiler State
# ----------------------------

current_temp = 0
target_temp = 100

# Initialize boiler status
db.child("boiler").child("status").update({
	"status": "ready",
	"temperature": current_temp,
	"target_temp": target_temp,
	"timestamp": time.time()
})

# ----------------------------
# Heating Function
# ----------------------------

def heat_enable():
	global current_temp
	print("Heating")
	current_temp += 10

# ----------------------------
# Process Order
# ----------------------------

def process_order(order_id):
	global current_temp

	print(f"Processing order: {order_id}")

	db.child("boiler").child("status").update({
		"status": "heating",
		"timestamp": time.time()
	})

	# Heat until target reached
	while current_temp < target_temp:
		heat_enable()
		time.sleep(1)

		db.child("boiler").child("status").update({
			"temperature": current_temp,
			"timestamp": time.time()
		})
	print("Heating Done!")

	db.child("boiler").child("status").update({
		"status": "idle",
		"timestamp": time.time()
	})

	# Wait for garnish to complete
	while db.child("garnish").child("status").get().val() != "complete":
		time.sleep(1)

	db.child("boiler").child("status").update({
		"status": "ready",
		"timestamp": time.time()
	})
	print("Order finished!")

	current_temp = 0
	db.child("boiler").child("status").update({
	"temperature": current_temp,
	"timestamp": time.time()
	})	
	db.child("orders").child(order_id).remove()

# ----------------------------
# FIFO Order Processing
# ----------------------------

def process_pending_orders():
	orders = db.child("orders").get()


	if not orders.each():
		print("no orders")
		
		return

	pending_orders = []

	for order in orders.each():
		order_id = order.key()
		status = db.child("orders").child(order_id).child("status").get().val()
		created_at = db.child("orders").child(order_id).child("time_stamp").get().val() or 0
		if status == "pending":
			pending_orders.append((order_id, created_at))
			# FIFO sort
			pending_orders.sort(key=lambda x: x[1])

	for order_id, _ in pending_orders:
		try:
		
			process_order(order_id)

		except Exception as e:
			print(f"Error processing {order_id}: {e}")

# ----------------------------
# Main Loop
# ----------------------------

if __name__ == "__main__":
	print("Listening for pending orders...")

	while True:
		process_pending_orders()
		time.sleep(5)
