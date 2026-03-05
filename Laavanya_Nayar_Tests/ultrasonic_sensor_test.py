from gpiozero import DistanceSensor
from time import sleep

# Updated to avoid Sense HAT Joystick pins
# trigger=17, echo=27
sensor = DistanceSensor(echo=27, trigger=17)

print("Ultrasonic Sensor Test (Sense HAT Safe)")

try:
    while True:
        cm = sensor.distance * 100
        print(f"Distance: {cm:.2f} cm")
        sleep(0.5)
except KeyboardInterrupt:
    print("Test Stopped")
