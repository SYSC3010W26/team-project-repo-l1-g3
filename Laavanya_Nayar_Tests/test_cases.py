import unittest
import time
import firebase_admin
from firebase_admin import credentials, db

# --- CONFIGURATION ---
DATABASE_URL = "https://soupercomputer-f0dad-default-rtdb.firebaseio.com/"

class TestGarnishNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests. Connects to DB."""
        if not firebase_admin._apps:
            cred = credentials.Certificate("soupercomputer-f0dad-firebase-adminsdk-fbsvc-9d52dc6494.json")
            firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
        print("\n>>> STARTING AUTOMATED TEST SUITE <<<")

    def setUp(self):
        """Runs before EACH test. Resets DB to clean state."""
        print(f"\n--- Setting up Test: {self._testMethodName} ---")
        ref = db.reference('/')
        ref.update({
            "mixer": {"status": "idle"},
            "garnish": {"status": "idle"},
            "orders": {
                "1": {
                    "toppings": ["init"],
                    "status": "pending"
                }
            },
            # Reset the simulated hardware sensor to 'Bowl Present' (5cm)
            "sim_hardware": {"distance": 5.0} 
        })
        time.sleep(1) # Give DB time to sync

    def test_01_happy_path(self):
        """Test Case 1: Standard Order with Toppings + Bowl Present"""
        print("SCENARIO: Mixer finishes, Toppings requested, Bowl is there.")
        
        # 1. Setup Order
        db.reference('/orders/1/toppings').set(["Onions", "Croutons"])
        
        # 2. Trigger Mixer Completion
        db.reference('/mixer/status').set("complete")
        
        print("Waiting for Garnish Node to react...")
        time.sleep(4) # Wait for simulation loop + servo delay
        
        # 3. Assert Result
        status = db.reference('/garnish/status').get()
        self.assertEqual(status, "complete", "Garnish should be complete")
        print("PASS: System dispensed toppings successfully.")

    def test_02_no_toppings(self):
        """Test Case 2: Order has NO toppings"""
        print("SCENARIO: Mixer finishes, but User wanted NO toppings.")
        
        # 1. Setup Empty Toppings
        db.reference('/orders/1/toppings').set([])
        
        # 2. Trigger Mixer
        db.reference('/mixer/status').set("complete")
        
        time.sleep(2)
        
        # 3. Assert Result
        status = db.reference('/garnish/status').get()
        self.assertEqual(status, "complete", "Garnish should complete (skip logic)")
        print("PASS: System skipped dispensing but marked complete.")

    def test_03_safety_no_bowl(self):
        """Test Case 3: Bowl is Missing (Safety Interlock)"""
        print("SCENARIO: Mixer finishes, but someone stole the bowl.")
        
        # 1. Hardware Simulation: Remove Bowl (Set distance to 50cm)
        db.reference('/sim_hardware/distance').set(50.0)
        
        # 2. Setup Order
        db.reference('/orders/1/toppings').set(["Onions"])
        
        # 3. Trigger Mixer
        db.reference('/mixer/status').set("complete")
        
        time.sleep(2)
        
        # 4. Assert Result
        status = db.reference('/garnish/status').get()
        self.assertEqual(status, "error", "Status should be error due to missing bowl")
        print("PASS: Safety interlock triggered. No toppings dispensed.")

if __name__ == '__main__':
    unittest.main()
