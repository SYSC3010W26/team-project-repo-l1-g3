## Weekly Individual Project Update Report
### Group number: L1G3
### Student name: Annan Jiang
### Week: Week 10
___
1. **How many hours did you spend on the project this week? (0-10)**
8 hours

2. **Give rough breakdown of hours spent on 1-3 of the following:**
   1. Testing: 4 hours (Wrote and ran unit tests for db.py, kiosk.py, and scanner.py covering database logic, order fulfillment, component status, and QR scan cooldown logic using mocked hardware and Firebase dependencies)
   2. Hardware implementation: 2 hours (Integrated emergency stop button on GPIO 23 with internal pull-down resistor; wired physical button on breadboard)
   3. Software implementation: 2 hours (Implemented emergency stop handler, Firebase system status tracking, and startup recovery logic for interrupted orders)

3. **What did you accomplish this week?**
   Implemented a hardware emergency stop button connected to GPIO 23 that immediately halts the kiosk, cancels any in-progress order, and writes an "emergency" status to Firebase /system/status. Added startup recovery logic so that on next boot, the system automatically detects the emergency state, cancels any stuck processing orders, and restores the system to "online". Wrote a full unit test suite (test_all.py) covering 15 test cases across all three core modules, with all hardware and Firebase dependencies mocked out so tests run entirely without physical hardware.

4. **How do you feel about your progress?**
   Good progress this week. The emergency stop feature adds meaningful fault tolerance to the system, and having a unit test suite gives confidence that core logic is correct without needing manual end-to-end testing every time.

5. **What are you planning to do next week?**
   Run full integration testing with all four nodes active. Validate the emergency stop behavior in a live system scenario. Finalize documentation and prepare for the final demonstration.

6. **Is anything blocking you that you need from others?**
   Currently resolving a GPIO edge detection conflict on the Raspberry Pi that prevents kiosk.py from starting cleanly after an unclean shutdown — investigating proper cleanup handling.
