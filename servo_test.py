from adafruit_servokit import ServoKit
import time

myKit = ServoKit(channels=16)
myKit.servo[0].set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
myKit.servo[0].actuation_range = 270
myKit.servo[1].set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
myKit.servo[1].actuation_range = 270
myKit.servo[2].set_pulse_width_range(min_pulse = 500, max_pulse = 2500)
myKit.servo[2].actuation_range = 270
myKit.servo[3].set_pulse_width_range(min_pulse = 1000, max_pulse = 2000)
myKit.servo[3].actuation_range = 180

rot_servo = myKit.servo[0]
lean_servo = myKit.servo[1]
elav_servo = myKit.servo[2]
jaws_servo = myKit.servo[3]

#Initial positions
rot_servo.angle = 135
lean_servo.angle = 135
elav_servo.angle = 135
jaws_servo.angle = 110