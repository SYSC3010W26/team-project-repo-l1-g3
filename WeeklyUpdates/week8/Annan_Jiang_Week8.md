## Weekly Individual Project Update Report
### Group number: L1G3
### Student name: Annan Jiang
### Week: Week8
___
1. **How many hours did you spend on the project this week? (0-10)**
8 hours

2. **Give rough breakdown of hours spent on 1-3 of the following:**
   (meetings, information gathering, design, research, brainstorming, evaluating options, prototyping options, writing/documenting, refactoring, testing, software implementation, hardware implementation)
   1. Testing: 5 hours (End-to-end firewall testing across all four Raspberry Pi nodes, validating data flow and connectivity)
   2. Meetings: 2 hours (Coordinating test plan with teammates, discussing results and next steps)
   3. Software implementation: 1 hour (Minor adjustments to communication protocols based on test findings)

3. **What did you accomplish this week?**
   Conducted comprehensive end-to-end testing across all four Raspberry Pi nodes (KIOSK, BOILER, MIXER, GARNISH) with firewall constraints in place.
   Verified successful information flow between all nodes despite firewall restrictions, confirming our Firebase-based communication architecture is robust.
   Validated that inter-node UART and Firebase message passing work reliably under realistic network conditions.
   Identified and documented any latency or data loss issues for future optimization.

4. **How do you feel about your progress?**
   Very positive. The end-to-end testing confirmed that our distributed system design is sound. Knowing that all four nodes can communicate reliably under firewall constraints gives me confidence in the system's resilience for the final demonstration.

5. **What are you planning to do next week?**
   Optimize message handling based on any bottlenecks discovered during testing.
   Begin integration testing with actual sensor input and motor control feedback loops.
   Refine error handling and retry logic for edge cases.
   Prepare documentation of test results and system validation for the final project report.

6. **Is anything blocking you that you need from others?**
   Need final confirmation from hardware team on sensor calibration values to incorporate into the control logic during next week's integration phase.
