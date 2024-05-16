import RPi.GPIO as gpio
import time

default_speed = 40

class MotorControl():
    def __init__(self):
        #Left motor
        # 27 - In 1 - Motor 1 - Green
        self.p_in1 = 27
        # 17 - In 2 - Motor 1 - Yellow
        self.p_in2 = 17
        # 13 (pwm) - ENA - Motor 1 - Blue
        self.p_ena = 13

        #right motor
        # 24 - In 3 - Motor 2 - White furthest from green
        self.p_in3 = 24
        # 23 - In 4 - Motor 2 - White closest to green
        self.p_in4 = 23
        # 12 (pwm) - ENB - Motor 2 - Purple
        self.p_enb = 12

        gpio.setwarnings(False) # The code is complaining too much
    
        gpio.setmode(gpio.BCM)
        gpio.setup(self.p_in1, gpio.OUT)
        gpio.setup(self.p_in2, gpio.OUT)
        gpio.setup(self.p_in3, gpio.OUT)
        gpio.setup(self.p_in4, gpio.OUT)
        
        gpio.setup(self.p_ena, gpio.OUT)
        gpio.setup(self.p_enb, gpio.OUT)

        self.p_a = gpio.PWM(self.p_ena,default_speed)
        self.p_b = gpio.PWM(self.p_enb,default_speed)

        self.p_a.start(0)
        self.p_b.start(0)

    # def forward(self):
    #     print('forward')
    #     gpio.output(self.p_in1, False)
    #     gpio.output(self.p_in2, True)
    #     gpio.output(self.p_in3, True)
    #     gpio.output(self.p_in4, False)
 

    # def reverse(self):
    #     print('reverse')
    #     gpio.output(self.p_in1, True)
    #     gpio.output(self.p_in2, False)
    #     gpio.output(self.p_in3, False)
    #     gpio.output(self.p_in4, True)    

    def forward(self):
        print('forward')
        gpio.output(self.p_in1, False)
        gpio.output(self.p_in2, True)
        gpio.output(self.p_in3, False)
        gpio.output(self.p_in4, True)
        # time.sleep(sec)
        # gpio.cleanup() 
    def reverse(self):
        print('reverse')
        gpio.output(self.p_in1, True)
        gpio.output(self.p_in2, False)
        gpio.output(self.p_in3, True)
        gpio.output(self.p_in4, False)
        # time.sleep(sec)
        # gpio.cleanup()


    def change_speed(self, pwm):
        # print('Speed: ', pwm)
        
        self.p_a.ChangeDutyCycle(pwm)
        self.p_b.ChangeDutyCycle(pwm)


    def turn_right(self, angle):
        print('right')
        speed = 1 - (-angle / 90) * default_speed
        # print(speed)
        self.p_a.ChangeDutyCycle(100)
        self.p_b.ChangeDutyCycle(speed)
        time.sleep(0.1)
        self.p_b.ChangeDutyCycle(100)


    def turn_left(self, angle):
        print('left')
        speed = 1 - (angle / 90) * default_speed
        # print(speed)
        self.p_a.ChangeDutyCycle(speed)
        self.p_b.ChangeDutyCycle(100)
        time.sleep(0.1)
        self.p_a.ChangeDutyCycle(100)
    


    def course_correction(self, bound):
        #if approaching left line
        if bound:
            self.p_a.ChangeDutyCycle(100)
            self.p_b.ChangeDutyCycle(90)
            time.sleep(0.1)
            self.p_b.ChangeDutyCycle(100)
            time.sleep(0.5)

        #if approaching right line
        else:
            self.p_a.ChangeDutyCycle(90)
            self.p_b.ChangeDutyCycle(100)
            time.sleep(0.1)
            self.p_a.ChangeDutyCycle(100)
            time.sleep(0.5)

    def stop(self):
        gpio.cleanup()







