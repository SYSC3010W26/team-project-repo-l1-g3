import pyrebase
import time
import temp_sensor
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

def verify_equal(a,b):
	if a == b:
		print("Test passed! Sensor Temperature: " + str(a) + " Database Temperature: " + str(b));
	else:
		print("Test failed! Sensor Temperature: " + str(a) + " Database Temperature: " + str(b));

while True:
	current_temp = temp_sensor.read()
	db.child("boiler").child("status").update({"temperature": current_temp,"timestamp": time.time()})
	db_temp = db.child("boiler").child("status").child("temperature").get().val()
	verify_equal(current_temp, db_temp)
	time.sleep(1)
	
	
	
