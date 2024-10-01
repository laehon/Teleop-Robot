import time
import threading
import Jetson.GPIO as GPIO
import pygame
import math

# Constants
PWM_FREQUENCY = 1000  # 1 kHz
PWM_PERIOD = 1 / PWM_FREQUENCY  # PWM period in seconds

class SoftwarePWM:
    def __init__(self, pin):
        self.pin = pin
        self.duty_cycle = 0  # Duty cycle percentage (0-100)
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.pwm_loop).start()

    def stop(self):
        self.running = False
        self.duty_cycle = 0

    def pwm_loop(self):
        while self.running:
            # Calculate the high time and low time based on duty cycle
            high_time = PWM_PERIOD * (self.duty_cycle / 100)
            low_time = PWM_PERIOD * ((100 - self.duty_cycle) / 100)

            # Turn the pin HIGH and sleep for the high time
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(high_time)

            # Turn the pin LOW and sleep for the low time
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(low_time)

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = max(0, min(duty_cycle, 100))  # Clamp to 0-100

class Motor:
    def __init__(self, pwm_pin, in1_pin, in2_pin):
        # Initialize GPIO pins
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

        # Initialize SoftwarePWM for speed control
        self.pwm = SoftwarePWM(pwm_pin)
        self.pwm.start()

    def set_speed(self, speed):
        """Set the motor speed. -100 to 100, where negative is reverse, positive is forward."""
        if speed > 0:
            # Forward: IN1 HIGH, IN2 LOW
            GPIO.output(self.in1_pin, GPIO.HIGH)
            GPIO.output(self.in2_pin, GPIO.LOW)
            self.pwm.set_duty_cycle(speed)  # Set duty cycle for forward speed
        elif speed < 0:
            # Reverse: IN1 LOW, IN2 HIGH
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.HIGH)
            self.pwm.set_duty_cycle(-speed)  # Set duty cycle for reverse speed
        else:
            # Stop the motor: IN1 LOW, IN2 LOW
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.LOW)
            self.pwm.set_duty_cycle(0)  # Stop the PWM signal


pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
joystick.init()
joy1_x = 0
joy1_y = 0
joy2_x = 0

DEAD_ZONE = 0.1

GPIO.setmode(GPIO.BOARD)

backleft = Motor(pwm_pin=33, in1_pin=37, in2_pin=35)
backright = Motor(pwm_pin=36, in1_pin=38, in2_pin=40)
frontleft = Motor(pwm_pin=11, in1_pin=15, in2_pin=13)
frontright = Motor(pwm_pin=22, in1_pin=24, in2_pin=26)

SPEED_STEP = 0.1

backleft_speed = 0
backright_speed = 0
frontleft_speed = 0
frontright_speed = 0

while True:
    
    pygame.event.pump()

    joy1_x = joystick.get_axis(0)
    joy1_y = -joystick.get_axis(1)
    joy2_x = joystick.get_axis(3)
    if abs(joy1_x) < DEAD_ZONE:
        joy1_x = 0
    if abs(joy1_y) < DEAD_ZONE:
        joy1_y = 0
    if abs(joy2_x) < DEAD_ZONE:
        joy2_x = 0

    theta = math.atan2(joy1_y, joy1_x)
    power = math.hypot(joy1_x, joy1_y)

    sin = math.sin(theta - math.pi/4)
    cos = math.cos(theta - math.pi/4)
    maximum = max(abs(sin), abs(cos))
    
    backleft_speed = (power * sin/maximum + joy2_x) * 100
    backright_speed = (power * cos/maximum - joy2_x) * 100
    frontleft_speed = (power * cos/maximum + joy2_x) * 100
    frontright_speed = (power * sin/maximum - joy2_x) * 100

    if (power + abs(joy2_x)) > 1:
        factor = power + abs(joy2_x)  # Precompute the normalization factor

        backleft_speed /= factor
        backright_speed /= factor
        frontleft_speed /= factor
        frontright_speed /= factor

    backleft.set_speed(backleft_speed)
    backright.set_speed(backright_speed)
    frontleft.set_speed(frontleft_speed)
    frontright.set_speed(frontright_speed)

    if joystick.get_button(4) == 1:
        print("Exiting...")
        break


# Cleanup
backleft.pwm.stop()
backright.pwm.stop()
frontleft.pwm.stop()
frontright.pwm.stop()
time.sleep(0.5)
GPIO.cleanup()
