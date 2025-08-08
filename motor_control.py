#!/usr/bin/env python3
# 1️⃣ Import Libraries
from gpiozero import Motor
from time import sleep

# 2️⃣ Set Up the Motors with PWM (BCM pin numbering)
left_motor = Motor(forward=20, backward=9, pwm=True)
right_motor = Motor(forward=6, backward=5, pwm=True)

# 3️⃣ Define Movement Functions
def forward(speed=1.0):
    left_motor.forward(speed)
    right_motor.forward(speed)

def backward(speed=1.0):
    left_motor.backward(speed)
    right_motor.backward(speed)

def left(speed=1.0):
    left_motor.backward(speed)
    right_motor.forward(speed)

def right(speed=1.0):
    left_motor.forward(speed)
    right_motor.backward(speed)

def stop():
    left_motor.stop()
    right_motor.stop()

# 4️⃣ Test Movement in a Sequence
def demo_sequence():
    forward(0.5)
    sleep(2)

    backward(0.5)
    sleep(2)

    left(0.5)
    sleep(1)

    right(0.5)
    sleep(1)

    stop()

if __name__ == "__main__":
    try:
        demo_sequence()
    except KeyboardInterrupt:
        pass
    finally:
        stop()
