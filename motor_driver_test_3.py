# Pins: 

# 27 - In 1 - Motor 1 - Green - Left
p_in1 = 27
# 17 - In 2 - Motor 1 - Yellow - Left
p_in2 = 17
# 24 - In 3 - Motor 2 - White furthest from green - Right
p_in3 = 24
# 23 - In 4 - Motor 2 - White closest to green - Right
p_in4 = 23

# 13 (pwm) - ENA - Motor 1 - Blue
p_ena = 13
# 12 (pwm) - ENB - Motor 2 - Purple 
p_enb = 12

max_speed = 100
global_multiplier = 0.5

import RPi.GPIO as gpio
import time

def init():    
    
    gpio.setwarnings(False) # The code is complaining too much
    
    gpio.setmode(gpio.BCM)
    gpio.setup(p_in1, gpio.OUT)
    gpio.setup(p_in2, gpio.OUT)
    gpio.setup(p_in3, gpio.OUT)
    gpio.setup(p_in4, gpio.OUT)
    
    gpio.setup(p_ena, gpio.OUT)
    gpio.setup(p_enb, gpio.OUT)

def change_speed_a(speed):
    # print('Speed a: ', speed)
    p_a.ChangeDutyCycle(speed)
def change_speed_b(speed):
    # print('Speed b: ', speed)
    p_b.ChangeDutyCycle(speed)

def setpins(pin_input):

    if pin_input[0] == 'f':
        gpio.output(p_in1, False)
    elif pin_input[0] == 't':
        gpio.output(p_in1, True)

    if pin_input[1] == 'f':
        gpio.output(p_in2, False)
    elif pin_input[1] == 't':
        gpio.output(p_in2, True)

    if pin_input[2] == 'f':
        gpio.output(p_in3, False)
    elif pin_input[2] == 't':
        gpio.output(p_in3, True)

    if pin_input[3] == 'f':
        gpio.output(p_in4, False)
    elif pin_input[3] == 't':
        gpio.output(p_in4, True)

def setspeed(speed_a, speed_b):
    p_a.ChangeDutyCycle(speed_a)
    p_b.ChangeDutyCycle(speed_b)

# Forward 
def Forward():
    
    print('forward')

    setpins('ftft')

    # gpio.output(p_in1, False)
    # gpio.output(p_in2, True)
    # gpio.output(p_in3, False)
    # gpio.output(p_in4, True)

    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

# Backward 
def Backward():
    print('backward')

    setpins('tftf')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

# Right
def Right():
    print('right')

    setpins('fttf')
    setspeed(global_multiplier * max_speed, 0)

# Left
def Left():
    print('left')

    setpins('ftft')
    setspeed(0, global_multiplier * max_speed)

def Stop():
    print('stop')

    setpins('tftf')
    setspeed(0, 0)

def Right_soft():
    print('right soft')

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

    time.sleep(1 / global_multiplier)

    setpins('fttf')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

    time.sleep(0.2 / global_multiplier)

def Right_medium():
    print('right medium')

    setpins('ftft')
    setspeed(int(0.66 * global_multiplier * max_speed), global_multiplier * max_speed)

def Left_soft():
    print('left soft')

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

    time.sleep(1 / global_multiplier)

    setpins('tfft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)

    time.sleep(0.2 / global_multiplier)

def Left_medium():
    print('left medium')

    setpins('ftft')
    setspeed(global_multiplier * max_speed, int(0.66 * global_multiplier * max_speed))

def Object():
    print('object')

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)
    
    setpins('tfft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1.1 / global_multiplier)

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1 / global_multiplier)

    setpins('fttf')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1 / global_multiplier)

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1.4 / global_multiplier)

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)

    setpins('fttf')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1.4 / global_multiplier)

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(0.8 / global_multiplier)

    setspeed(0, 0)
    time.sleep(0.4 / global_multiplier)

    setpins('tfft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(1 / global_multiplier)

    setpins('ftft')
    setspeed(global_multiplier * max_speed, global_multiplier * max_speed)
    time.sleep(0.2 / global_multiplier)


init()
p_a = gpio.PWM(p_ena,global_multiplier * max_speed)
p_b = gpio.PWM(p_enb,global_multiplier * max_speed)

p_a.start(0)
p_b.start(0)

change_speed_a(0)
change_speed_b(0)

while True:
    command = input('Give input: ')
    
    if command == 't':
        Forward()
    elif command == 'f':
        Left()
    elif command == 'g':
        Backward()
    elif command == 'h':
        Right()
    elif command == 'a':
        Stop()
    elif command == 'd':
        Left_soft()
    elif command == 's':
        Left_medium()
    elif command == 'j':
        Right_soft()
    elif command == 'k':
        Right_medium()
    elif command == 'o':
        Object()
    elif command == 'l':
        speed_command = input('Give speed (0 - 100): ')
        change_speed_a(int(speed_command))
    elif command == 'p':
        speed_command = input('Give speed (0 - 100): ')
        change_speed_b(int(speed_command))
    elif command == 'm':
        global_multiplier = float(input('Give multiplier (0 - 1): '))
    elif command == 'q':
        gpio.cleanup()
        exit()
    else:
        print('Bad command')
        gpio.cleanup()
        exit()









# //Left

# void Right(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, HIGH);
#   digitalWrite(LowR, LOW);
#   analogWrite(EnL,230);
#   analogWrite(EnR, 0);

# }
# void Left(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 0);
#   analogWrite(EnR,230);

# }
# void Stop(){
#   digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, HIGH);
#   digitalWrite(LowR, LOW);
#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);

# }
# void Right_soft(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnR,255);
#   analogWrite(EnL,255);
#   delay(1000);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, HIGH);
#   digitalWrite(LowR, LOW);
#   analogWrite(EnR,255);
#   analogWrite(EnL,255);
#   delay(200);

#  }

#  void Right_medium(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnR,170);
#   analogWrite(EnL,255);


#  }
#  void Left_soft(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnR,255);
#   analogWrite(EnL,255);
#       delay(1000);
#   digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnR,255);
#   analogWrite(EnL,255);
#     delay(200);

#  }

#  void Left_medium(){
#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnR,255);
#   analogWrite(EnL,170);



#  }

#  void Object(){
  
#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);



#   digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, LOW);    //left
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1100);
  
#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 250);
#   analogWrite(EnR, 250);
#   delay(1000);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, HIGH);    //Right
#   digitalWrite(LowR, LOW);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1000);

#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 250);
#   analogWrite(EnR, 250);
#   delay(1400);

#   analogWrite(EnL, 0); 
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, HIGH);    //Right
#   digitalWrite(LowR, LOW);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1400);

#   analogWrite(EnL, 0); 
#   analogWrite(EnR, 0);
#   delay(400);
#     digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 250);
#   analogWrite(EnR, 250);
#   delay(800);
#     analogWrite(EnL, 0); 
#   analogWrite(EnR, 0);
#   delay(400);

#     digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, LOW);    //left
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1000);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR, 255);
#   delay(200);
  
#   }

# void UTurn(){
#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);

#   analogWrite(EnL, 250);
#   analogWrite(EnR, 250);
#   delay(1700);
  
#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, LOW);    //left
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1800);

#   analogWrite(EnL, 0);
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 250);
#   analogWrite(EnR, 250);
#   delay(900);

#   analogWrite(EnL, 0); 
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, HIGH);
#   digitalWrite(LowL, LOW);
#   digitalWrite(HighR, LOW);    //left
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR,255);
#   delay(1000);

#   analogWrite(EnL, 0); 
#   analogWrite(EnR, 0);
#   delay(400);

#   digitalWrite(HighL, LOW);
#   digitalWrite(LowL, HIGH);
#   digitalWrite(HighR, LOW);   //Forward
#   digitalWrite(LowR, HIGH);
#   analogWrite(EnL, 255);
#   analogWrite(EnR, 255);
#   delay(200);
#   }
# void StopS(){
#       analogWrite(EnL, 0);
#       analogWrite(EnR, 0);
#       delay(4500);
#       analogWrite(EnL, 250);
#       analogWrite(EnR, 250);
#       delay(1000);
#       }
# void loop() {


#   Data();
#   if (binary == 0){
#     Forward();
#     }
#    else if(binary == 1){
#     Right_medium();
#     }
#    else if(binary == 2){
#      Right();
#     }
#    else if(binary == 3){
#     Right();
#     }
#   else if(binary == 4){
#     Left_medium();
#     }
#    else if(binary == 5){
#     Left();
#     }
#    else if(binary == 6){
#     Left();
#     }
#     else if(binary == 7){
#     UTurn();
#     }
#     else if(binary == 8){
#      StopS();
#     }
#     else if(binary == 9){
#     Object();
#     }
#     else if(binary > 9){
#     Stop();
#     }

# }