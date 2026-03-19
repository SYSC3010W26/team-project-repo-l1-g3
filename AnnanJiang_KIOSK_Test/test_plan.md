# KIOSK End-to-End Communication Test Plan

## Objective
Verify that KIOSK can successfully submit orders and receive status updates from other kitchen nodes through Firebase database.

## Test Cases

### Test 1: Submit Order
- **Purpose**: Verify KIOSK can submit order to database
- **Input**: Order with soup type, toppings, price
- **Expected**: Order stored in database with correct data
- **Verification**: Query database and confirm order exists

### Test 2: Multiple Orders
- **Purpose**: Verify KIOSK can handle multiple orders
- **Input**: Submit 3 different orders
- **Expected**: All 3 orders stored in database
- **Verification**: Count orders in database

### Test 3: Data Integrity
- **Purpose**: Verify all order fields are stored correctly
- **Input**: Order with multiple toppings and price
- **Expected**: All fields match submitted data
- **Verification**: Check each field: soup type, toppings count, price

### Test 4: Status Update
- **Purpose**: Verify KIOSK can receive order status updates
- **Input**: Update order status from "pending" to "ready"
- **Expected**: Status change reflected in database
- **Verification**: Query order and check status field

## End-to-End Communication Flow
1. KIOSK submits order to Firebase
2. Database stores order
3. KIOSK listens to boiler/mixer/garnish nodes
4. KIOSK receives status updates from other nodes
5. KIOSK updates order status in database

## Test Execution
Run: `python kiosk_test.py`
All 4 tests must pass to verify end-to-end communication works.
