import time
from adafruit_servokit import ServoKit
import pygame

# Initialize the ServoKit class for a 16-channel PWM controller
kit = ServoKit(channels=16)

# Define servos
rot_servo = kit.servo[0]
lean_servo = kit.servo[1]
elav_servo = kit.servo[2]
jaws_servo = kit.servo[3]

# Set bounds for servo
rot_servo.set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
rot_servo.actuation_range = 270
lean_servo.set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
lean_servo.actuation_range = 270
elav_servo.set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
elav_servo.actuation_range = 270
jaws_servo.set_pulse_width_range(min_pulse = 1000, max_pulse = 2000)
jaws_servo.actuation_range = 180

#Initial positions
rot_servo.angle = 135
lean_servo.angle = 135
elav_servo.angle = 135
jaws_servo.angle = 130

rot_angle = 135
lean_angle = 135
elev_angle = 135
step_size = 0.25

# Define the limits
ROT_MIN = 0
ROT_MAX = 270
LEAN_MIN = 95
LEAN_MAX = 196
ELEV_MIN = 88
ELEV_MAX = 189
SUM_MIN = 244
SUM_MAX = 358

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
joystick.init()

print("Initialized")

# lean_servo: 95 to 196 (118) (190)
# elev_servo: 88 to 189 (126) (168)

while True:

    pygame.event.pump()

    if joystick.get_hat(0)[1] == 1:
        new_lean_angle = min(LEAN_MAX, lean_angle + step_size)
        if SUM_MIN <= new_lean_angle + elev_angle <= SUM_MAX:
            lean_angle = new_lean_angle

    if joystick.get_hat(0)[1] == -1:
        new_lean_angle = max(LEAN_MIN, lean_angle - step_size)
        if SUM_MIN <= new_lean_angle + elev_angle <= SUM_MAX:
            lean_angle = new_lean_angle
        
    if joystick.get_hat(0)[0] == -1:
        rot_angle = max(ROT_MIN, rot_angle - 2*step_size)

    if joystick.get_hat(0)[0] == 1:
        rot_angle = min(ROT_MAX, rot_angle + 2*step_size)      
        
    if joystick.get_button(3) == 1:
        new_elev_angle = min(ELEV_MAX, elev_angle + step_size)
        if SUM_MIN <= lean_angle + new_elev_angle <= SUM_MAX:
            elev_angle = new_elev_angle

    if joystick.get_button(2) == 1:
        new_elev_angle = max(ELEV_MIN, elev_angle - step_size)
        if SUM_MIN <= lean_angle + new_elev_angle <= SUM_MAX:
            elev_angle = new_elev_angle

    if joystick.get_button(0) == 1:
        jaws_servo.angle = 80
    
    if joystick.get_button(1) == 1:
        jaws_servo.angle = 130
    
    lean_servo.angle = lean_angle
    elav_servo.angle = elev_angle
    rot_servo.angle = rot_angle

    if joystick.get_button(4) == 1:
        print("Exiting...")
        break
    


