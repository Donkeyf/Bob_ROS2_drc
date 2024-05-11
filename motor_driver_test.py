# Pins: 

# 27 - In 1 - Motor 1 - Green
p_in1 = 27
# 17 - In 2 - Motor 1 - Yellow
p_in2 = 17
# 24 - In 3 - Motor 2 - White furthest from green
p_in3 = 24
# 23 - In 4 - Motor 2 - White closest to green
p_in4 = 23

# 13 (pwm) - ENA - Motor 1 - Blue
p_ena = 13
# 12 (pwm) - ENB - Motor 2 - Purple
p_enb = 12

import RPi.GPIO as gpio
import time

# from gpiozero import Motor

def init():    
    
    gpio.setwarnings(False) # The code is complaining too much
    
    gpio.setmode(gpio.BCM)
    gpio.setup(p_in1, gpio.OUT)
    gpio.setup(p_in2, gpio.OUT)
    gpio.setup(p_in3, gpio.OUT)
    gpio.setup(p_in4, gpio.OUT)
    
    gpio.setup(p_ena, gpio.OUT)
    gpio.setup(p_enb, gpio.OUT)

def forward():
    print('forward')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)
    # time.sleep(sec)
    # gpio.cleanup() 
def reverse():
    print('reverse')
    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)
    # time.sleep(sec)
    # gpio.cleanup()
def left_turn():
    print('left')
    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)
    # time.sleep(sec)
    # gpio.cleanup()
def right_turn():
    print('right')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)
    # time.sleep(sec)
    # gpio.cleanup()
def change_speed(speed):
    print('Speed: ', speed)
    
    p_a.ChangeDutyCycle(speed)
    p_b.ChangeDutyCycle(speed)

init()
p_a = gpio.PWM(p_ena,100)
p_b = gpio.PWM(p_enb,100)

p_a.start(0)
p_b.start(0)

while True:
    command = input('Give input: ')
    
    if command == 'w':
        forward()
    elif command == 'a':
        left_turn()
    elif command == 's':
        reverse()
    elif command == 'd':
        right_turn()
    elif command == 'l':
        speed_command = input('Give speed (0 - 100): ')
        change_speed(int(speed_command))
    elif command == 'q':
        gpio.cleanup()
        exit()
    else:
        print('Bad command')
        exit()