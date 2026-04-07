# Souper Kiosk

**Course:** SYSC 3010  
**Group Number:** [L1 G3]  
**TA:** [Albert Lin]  

**Authuor:**
- Annan Jiang
---

## Project Summary

The Souper Kiosk is an automated soup vending system that allows customers to order customized soups through a mobile web interface and have them prepared and dispensed by a Raspberry Pi-controlled machine. Customers browse a menu of six soup bases (Chicken Broth, Tomato Soup, Beef Broth, Vegetable Soup, Mushroom Soup, Miso Soup) and six toppings (Broccoli, Carrots, Chicken, Tofu, Croutons, Cheese) via a Firebase-hosted webpage. Upon placing an order, a QR code is generated for the customer to use at pickup.

On the hardware side, a Raspberry Pi acts as the central controller, polling Firebase for new orders and coordinating three kitchen sub-components — a boiler, a mixer, and a garnish dispenser — to prepare each soup. Once the order is ready, the customer scans their QR code at a pickup station (also Raspberry Pi-powered with a camera) to retrieve their order. Green and red LEDs provide visual confirmation of valid or invalid scans.

Order history and inventory levels are tracked locally in an SQLite database, and a reporting tool allows monthly revenue and popularity statistics to be viewed at any time.

---

## Repository Structure

```
3010_Kiosk/
├── README.md                  # This file
└── Souper_Kiosk/              # Main application code
    ├── kiosk.py               # Main coordinator: polls Firebase, drives kitchen components
    ├── scanner.py             # Pickup station: scans QR codes, controls LEDs via GPIO
    ├── db.py                  # SQLite database module (orders, inventory, stats)
    ├── config.py              # Firebase project configuration
    ├── firebase.json          # Firebase hosting configuration
    ├── mobile.html            # Customer-facing ordering web interface
    ├── send_order.py          # Dev utility to push test orders to Firebase
    ├── watch_all.py           # Kitchen component status monitor
    ├── stats.py               # Monthly revenue and sales reporting CLI
    ├── test_all.py            # Unit test suite (mocked hardware/Firebase)
    ├── souper_qr.png          # QR code image used for ordering
    └── public/                # Firebase Hosting deployment directory
        ├── index.html         # Default hosting landing page
        └── mobile.html        # Deployed customer ordering interface
```

## How to Run

### 1. Start the Main Kiosk Controller (Raspberry Pi)
This process polls Firebase for new orders and coordinates kitchen hardware:
```bash
cd Souper_Kiosk
python kiosk.py
```

### 2. Start the Pickup Scanner (Raspberry Pi)
Run this on the pickup station Raspberry Pi (can be the same Pi):
```bash
python scanner.py
```

### 3. Customer Orders
Customers open the Firebase-hosted URL (from `firebase.json`) on their phone, select a soup and toppings, and place an order. A QR code is displayed upon order confirmation.

### 4. View Statistics
```bash
python stats.py
```

