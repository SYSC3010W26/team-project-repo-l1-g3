## Weekly Individual Project Update Report
### Group number: L1-G3
### Student name: Laavanya Nayar
### Week: 12 (Apr 1 – Apr 3)
___
1. **How many hours did you spend on the project this week? (0-10)**
   10 hours

2. **Give rough breakdown of hours spent on 1-3 of the following:**
   1. Prototyping Options: 5 hours (Attempted to pivot to a cardboard mechanical housing for the garnish indexer due to 3D printer unavailability in the lab).
   2. Testing: 3 hours (Validated the FIFO queue logic and the global "bowl_present" safety interlock via Firebase).
   3. Writing/Documenting: 2 hours (Contributing final observations and hardware troubleshooting notes to the Final Project Report).

3. ***What did you accomplish this week?*** _(Be specific)_
  - **Executed a Hardware Pivot:** Due to lack of 3D printer availability, I designed and constructed a rapid-prototype version of the disk indexer and topping hopper using reinforced cardboard and adhesive.
  - **Validated System Logic:** While the physical friction of the cardboard hindered mechanical consistency, I successfully proved the software logic. The Garnish node accurately read the `/orders/1` FIFO path and correctly broadcasted the `bowl_present` flag to the Boiler and Mixer nodes.
  - **Final Demonstration:** Presented the SouperComputer to the TA. Although the mechanical sequence was not fully completed due to cardboard rigidity issues, I provided a thorough technical defense of the distributed architecture and cloud-based safety protocols.
  - **Passed the Technical Demo:** Effectively communicated the system's "Separation of Concerns" and asynchronous communication design to the TA, resulting in a successful demo pass.

4. ***How do you feel about your progress?*** _(brief, free-form reflection)_
  - This week was a lesson in engineering pragmatism. While I was disappointed that the 3D printer wasn't available, building the cardboard prototype helped me identify specific friction points that I wouldn't have noticed in a digital CAD model. I am proud that our system architecture was robust enough that we could explain and prove the logic to the TA despite the mechanical setbacks.

5. ***What are you planning to do next week***? _(give specific goals)_
  - Complete the final formatting of the Final Project Report.
  - Submit the final project deliverables before the April 6th deadline.

6. ***Is anything blocking you that you need from others?*** _(What do you need from whom)_
  - No blockers. The team is focused on the final report submission.
