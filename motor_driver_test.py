# Pins: 

# 27 - In 1 - Motor 1
p_in1 = 27
# 17 - In 2 - Motor 1
p_in2 = 17
# 24 - In 3 - Motor 2
p_in3 = 24
# 23 - In 4 - Motor 2
p_in4 = 23

# 13 (pwm) - ENA - Motor 1
p_ena = 13
# 12 (pwm) - ENB - Motor 2
p_enb = 12

import RPi.GPIO as gpio
import time

def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(p_in1, gpio.OUT)
    gpio.setup(p_in2, gpio.OUT)
    gpio.setup(p_in3, gpio.OUT)
    gpio.setup(p_in4, gpio.OUT)
    
    gpio.setup(p_ena, gpio.OUT)
    gpio.setup(p_enb, gpio.OUT)

def forward(sec):
    print('forward')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)
    time.sleep(sec)
    gpio.cleanup() 
def reverse(sec):
    print('reverse')
    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)
    time.sleep(sec)
    gpio.cleanup()
def left_turn(sec):
    print('left')
    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)
    time.sleep(sec)
    gpio.cleanup()
def right_turn(sec):
    print('right')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)
    time.sleep(sec)
    gpio.cleanup()
def change_speed(speed):
    print('speed:', speed)
    
    p_a.ChangeDutyCycle(speed)
    p_b.ChangeDutyCycle(speed)

init()
p_a = gpio.PWM(p_ena,1000)
p_b = gpio.PWM(p_enb,1000)

while True:
    command = input('Give input:')
    
    if command == 'w':
        forward(100)
    if command == 'a':
        left_turn(100)
    if command == 's':
        reverse(100)
    if command == 'd':
        right_turn(100)
    if command == 'l':
        speed_command = input('Give speed (0 - 100):')
        change_speed(speed_command)
    
    else:
        print('Bad command')
        exit()