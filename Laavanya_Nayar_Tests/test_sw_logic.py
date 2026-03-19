import unittest

# --- The Logic Functions from your main code (Isolated) ---
def is_bowl_present(distance_cm):
    """Business Logic: Bowl is present if distance is less than 10cm"""
    if distance_cm < 0:
        return False # Catch sensor glitches
    return distance_cm < 10.0

def should_garnish_run(mixer_status, toppings_list):
    """Business Logic: Only run if mixer is done AND toppings are requested"""
    if mixer_status != "complete":
        return False
    if not toppings_list or len(toppings_list) == 0:
        return False
    return True

# --- The Unit Tests ---
class TestGarnishSoftwareLogic(unittest.TestCase):
    
    def test_bowl_detection_logic(self):
        """Test the boundaries of the distance sensor logic"""
        self.assertTrue(is_bowl_present(5.0), "5cm should detect a bowl")
        self.assertTrue(is_bowl_present(9.9), "9.9cm should detect a bowl")
        self.assertFalse(is_bowl_present(10.1), "10.1cm should NOT detect a bowl")
        self.assertFalse(is_bowl_present(-5.0), "Negative numbers should be rejected")

    def test_garnish_decision_tree(self):
        """Test if the node correctly decides to skip or run"""
        # Case 1: Mixer done, wants onions
        self.assertTrue(should_garnish_run("complete", ["Onions"]))
        
        # Case 2: Mixer done, but no toppings requested
        self.assertFalse(should_garnish_run("complete",[]))
        
        # Case 3: Mixer still mixing, wants onions
        self.assertFalse(should_garnish_run("mixing", ["Onions"]))

if __name__ == '__main__':
    unittest.main()
