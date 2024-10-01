import pygame
import time

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()


# Check if any joysticks are connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
    pygame.quit()
else:
    print("Joystick detected!")
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()

while True:
    # Process events
    pygame.event.pump()  # Update the input events

    # Get axis values (e.g., analog sticks)
    for i in range(joystick.get_numaxes()):
        axis_value = joystick.get_axis(i)
        print(f"Axis {i}: {axis_value}")

    # Get button values (e.g., A, B, X, Y, triggers)
    for i in range(joystick.get_numbuttons()):
        button_value = joystick.get_button(i)
        print(f"Button {i}: {button_value}")

    # Get hat values (D-pad)
    for i in range(joystick.get_numhats()):
        hat_value = joystick.get_hat(i)
        print(f"Hat {i}: {hat_value}")

    # Sleep to prevent spamming the terminal
    time.sleep(0.1)

pygame.quit()
