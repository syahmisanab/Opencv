from gpiozero import Motor
import pygame
from time import sleep

left_motor = Motor(forward=20, backward=9, pwm=True)
right_motor = Motor(forward=6, backward=5, pwm=True)

def stop():
    left_motor.stop()
    right_motor.stop()

pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Motor Control")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_motor.forward()
                right_motor.forward()
            elif event.key == pygame.K_s:
                left_motor.backward()
                right_motor.backward()
            elif event.key == pygame.K_a:
                left_motor.backward()
                right_motor.forward()
            elif event.key == pygame.K_d:
                left_motor.forward()
                right_motor.backward()
            elif event.key == pygame.K_q:
                stop()
        elif event.type == pygame.KEYUP:
            stop()
    sleep(0.1)

stop()
pygame.quit()
