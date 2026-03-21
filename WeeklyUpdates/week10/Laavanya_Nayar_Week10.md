## Weekly Individual Project Update Report

**Group number:** L1-G3  
**Student name:** Laavanya Nayar  
**Week:** Week 10  

---

### 1. How many hours did you spend on the project this week? (0-10)
8 hours

---

### 2. Give rough breakdown of hours spent on 1-3 of the following:

- **Testing:** 4 hours  
  Wrote and executed a complete Unit Test Suite for the Garnish node, including isolated hardware tests for the servo/ultrasonic sensor, database integrity tests, and pure software logic tests.

- **Software implementation:** 2 hours  
  Refactored the Garnish node's main script to decouple the decision-making logic from the hardware execution, allowing for true separation of concerns during testing.

- **Hardware implementation:** 2 hours  
  Finalized the physical wiring, specifically testing and validating the voltage divider circuit on the HC-SR04 Echo pin to ensure safe 3.3V logic levels for the Raspberry Pi.

---

### 3. What did you accomplish this week? (Be specific)

- Created a comprehensive unit test suite to satisfy the Lab 10 requirements, proving that the Garnish Node works at the component level before full system integration.

- Wrote dedicated hardware drivers:
  - `test_hw_ultrasonic.py`
  - `test_hw_servo.py` 
  These verify PWM signals, I2C communication, and GPIO pin states independently.

- Developed `test_sw_logic.py` using the `unittest` framework to validate the `should_dispense_garnish()` decision matrix.  
  Confirmed correct handling of edge cases such as:
  - Missing bowl safety interlock  
  - Orders with zero toppings  
  - Premature mixer states  

- Successfully demonstrated these isolated unit tests to the TA.

---

### 4. How do you feel about your progress? (brief reflection)

I feel highly confident about our progress. Refactoring the code to support isolated unit testing forced cleaner, more modular design. Verifying safety interlocks in software gives confidence before integrating physical motors.

---

### 5. What are you planning to do next week? (specific goals)

- Mount the Garnish Node hardware (Pi, breadboard, servos) onto the final chassis.
- Conduct full physical integration testing with the Kiosk, Boiler, and Mixer nodes.
- Verify mechanical timing (e.g., toppings dispensing accurately into the cup).
- Begin contributing to the final project report and demo video planning.

---

### 6. Is anything blocking you?

No major software blockers. Need coordination with the team during physical assembly to ensure proper ultrasonic sensor placement and line-of-sight.
