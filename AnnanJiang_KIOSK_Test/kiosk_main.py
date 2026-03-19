import pyrebase
import time
import threading
from config import FIREBASE_CONFIG

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

class Kiosk:
    def __init__(self):
        self.streams = []
    
    def submit_order(self, soup_type, toppings, price):
        order_id = str(int(time.time() * 1000))
        order = {
            "order_id": order_id,
            "soup_type": soup_type,
            "toppings": toppings,
            "price": price,
            "status": "pending",
            "timestamp": time.time()
        }
        db.child("orders").child(order_id).set(order)
        print(f"Order submitted: {order_id}")
        return order_id
    
    def boiler_handler(self, msg):
        if msg["data"]:
            print(f"Boiler: {msg['data']}")
    
    def mixer_handler(self, msg):
        if msg["data"]:
            print(f"Mixer: {msg['data']}")
    
    def garnish_handler(self, msg):
        if msg["data"]:
            print(f"Garnish: {msg['data']}")
    
    def start_listening(self):
        try:
            stream1 = db.child("boiler").child("status").stream(self.boiler_handler)
            stream2 = db.child("mixer").child("status").stream(self.mixer_handler)
            stream3 = db.child("garnish").child("status").stream(self.garnish_handler)
            self.streams = [stream1, stream2, stream3]
            
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_listening()
    
    def stop_listening(self):
        for stream in self.streams:
            stream.close()
        print("Kiosk stopped")

if __name__ == "__main__":
    kiosk = Kiosk()
    listener = threading.Thread(target=kiosk.start_listening, daemon=True)
    listener.start()
    
    while True:
        print("\n=== Kiosk ===")
        print("1. Submit order")
        print("2. Exit")
        choice = input("Choose: ").strip()
        
        if choice == "1":
            soup = input("Soup type (miso/tonkotsu/shoyu/vegetable): ").strip()
            toppings_input = input("Toppings (comma separated): ").strip()
            toppings = [t.strip() for t in toppings_input.split(",")] if toppings_input else []
            
            try:
                price = float(input("Price: "))
                kiosk.submit_order(soup, toppings, price)
            except ValueError:
                print("Invalid price")
        else:
            break
