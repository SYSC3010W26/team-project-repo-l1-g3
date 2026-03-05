from gpiozero import Servo
from time import sleep

# GPIO 18 is safe with Sense HAT
servo = Servo(18)

try:
    for i in range(10):
        print("Servo Mid...")
        servo.mid()
        sleep(1)
        print("Servo Min...")
        servo.min()
        sleep(1)
        print("Servo Max...")
        servo.max()
        sleep(1)
except KeyboardInterrupt:
    servo.detach()
