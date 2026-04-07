import pyrebase
import time
from config import FIREBASE_CONFIG

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

class KioskTest:
    def __init__(self):
        self.results = []
    
    def test_submit_order(self):
        print("\nTest 1: Submit Order")
        
        order = {
            "order_id": "test_001",
            "soup_type": "miso",
            "toppings": ["egg"],
            "price": 9.99,
            "status": "pending",
            "timestamp": time.time()
        }
        
        db.child("orders").child("test_001").set(order)
        time.sleep(1)
        
        stored = db.child("orders").child("test_001").get()
        passed = stored.val() and stored.val()["soup_type"] == "miso"
        
        print("PASS" if passed else "FAIL")
        self.results.append(("Submit Order", passed))
        return passed
    
    def test_multiple_orders(self):
        print("\nTest 2: Multiple Orders")
        
        orders = ["test_002", "test_003", "test_004"]
        for oid in orders:
            db.child("orders").child(oid).set({
                "order_id": oid,
                "soup_type": "tonkotsu",
                "toppings": ["egg"],
                "price": 10.99,
                "status": "pending",
                "timestamp": time.time()
            })
        
        time.sleep(1)
        all_orders = db.child("orders").get()
        passed = all_orders.val() and len(all_orders.val()) >= 3
        
        print("PASS" if passed else "FAIL")
        self.results.append(("Multiple Orders", passed))
        return passed
    
    def test_data_integrity(self):
        print("\nTest 3: Data Integrity")
        
        order = {
            "order_id": "test_005",
            "soup_type": "miso",
            "toppings": ["egg", "nori", "pork"],
            "price": 12.99,
            "status": "pending",
            "timestamp": time.time()
        }
        
        db.child("orders").child("test_005").set(order)
        time.sleep(1)
        
        stored = db.child("orders").child("test_005").get().val()
        passed = (
            stored["soup_type"] == "miso" and
            len(stored["toppings"]) == 3 and
            stored["price"] == 12.99
        )
        
        print("PASS" if passed else "FAIL")
        self.results.append(("Data Integrity", passed))
        return passed
    
    def test_status_update(self):
        print("\nTest 4: Status Update")
        
        db.child("orders").child("test_006").set({
            "order_id": "test_006",
            "soup_type": "tonkotsu",
            "toppings": ["egg"],
            "price": 10.99,
            "status": "pending",
            "timestamp": time.time()
        })
        
        time.sleep(1)
        db.child("orders").child("test_006").update({"status": "ready"})
        time.sleep(1)
        
        updated = db.child("orders").child("test_006").get().val()
        passed = updated["status"] == "ready"
        
        print("PASS" if passed else "FAIL")
        self.results.append(("Status Update", passed))
        return passed
    
    def run_all(self):
        print("="*40)
        print("KIOSK End-to-End Communication Tests")
        print("="*40)
        
        self.test_submit_order()
        self.test_multiple_orders()
        self.test_data_integrity()
        self.test_status_update()
        
        print("\n" + "="*40)
        print("Results Summary")
        print("="*40)
        
        for name, passed in self.results:
            status = "PASS" if passed else "FAIL"
            print(f"{name:20} {status}")
        
        total = len(self.results)
        passed = sum(1 for _, p in self.results if p)
        print(f"\nTotal: {passed}/{total} tests passed")
        print("="*40)

if __name__ == "__main__":
    tester = KioskTest()
    tester.run_all()
