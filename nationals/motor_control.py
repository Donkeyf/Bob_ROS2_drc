import RPi.GPIO as gpio
import time

DEFAULT_SPEED = 10

class MotorControl():
    def __init__(self):
        '''
        Pin Assignment Declarations
        LEFT
        IN1 - 27 - Motor 1 - Green
        IN2 - 17 - Motor 1 - Yellow
        ENA - 13 - Motor 1 - Blue

        RIGHT
        IN3 - 24 - Motor 2 - White furthest from green
        IN4 - 23 - Motor 2 - White closest to green
        ENB - 12 - Motor 2 - Purple
        '''
        self.IN1 = 27
        self.IN2 = 17
        self.ENA = 13

        self.IN3 = 24
        self.IN4 = 23
        self.p_ENB = 12

        gpio.setwarnings(False) # The code is complaining too much
    
        gpio.setmode(gpio.BCM)
        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.IN3, gpio.OUT)
        gpio.setup(self.IN4, gpio.OUT)
        
        gpio.setup(self.ENA, gpio.OUT)
        gpio.setup(self.ENB, gpio.OUT)

        self.p_a = gpio.PWM(self.ENA, DEFAULT_SPEED)
        self.p_b = gpio.PWM(self.ENB, DEFAULT_SPEED)

        self.p_a.start(0)
        self.p_b.start(0)   

    def forward(self):
        print('Forward')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(250)
        self.p_b.ChangeDutyCycle(250)
        
    def reverse(self):
        print('Reverse')
        gpio.output(self.IN1, True)
        gpio.output(self.IN2, False)
        gpio.output(self.IN3, True)
        gpio.output(self.IN4, False)
        self.p_a.ChangeDutyCycle(250)
        self.p_b.ChangeDutyCycle(250)

    def soft_right(self):
        print('Soft Right')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(255)
        self.p_b.ChangeDutyCycle(255)
        time.sleep(1)

        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, True)
        gpio.output(self.IN4, False)
        self.p_a.ChangeDutyCycle(255)
        self.p_b.ChangeDutyCycle(255)
        time.sleep(0.2)

    def med_right(self):
        print('Medium Right')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(170)
        self.p_b.ChangeDutyCycle(255)

    def hard_right(self):
        print('Hard Right')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, True)
        gpio.output(self.IN4, False)
        self.p_a.ChangeDutyCycle(230)
        self.p_b.ChangeDutyCycle(0)

    def soft_left(self):
        print('Soft Left')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(255)
        self.p_b.ChangeDutyCycle(255)
        time.sleep(1)

        gpio.output(self.IN1, True)
        gpio.output(self.IN2, False)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(255)
        self.p_b.ChangeDutyCycle(255)
        time.sleep(0.2)

    def med_left(self):
        print('Medium Left')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, True)
        self.p_a.ChangeDutyCycle(255)
        self.p_b.ChangeDutyCycle(170)

    def hard_left(self):
        print('Hard Left')
        gpio.output(self.IN1, False)
        gpio.output(self.IN2, True)
        gpio.output(self.IN3, False)
        gpio.output(self.IN4, False)
        self.p_a.ChangeDutyCycle(0)
        self.p_b.ChangeDutyCycle(230)

    def stop(self):
        gpio.cleanup()







