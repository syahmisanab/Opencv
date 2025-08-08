from gpiozero import LED
from time import sleep

# Set up LED on GPIO 21 (physical pin 40)
led = LED(21)

try:
    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)
except KeyboardInterrupt:
    print("\nExiting program...")
