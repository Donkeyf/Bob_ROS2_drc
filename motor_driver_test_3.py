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

# Forward 
def Forward():
    
    print('forward')

    setpins('ftft')

    # gpio.output(p_in1, False)
    # gpio.output(p_in2, True)
    # gpio.output(p_in3, False)
    # gpio.output(p_in4, True)

    change_speed_a(100)
    change_speed_b(100)

# Backward 
def Backward():
    print('backward')
    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)

    change_speed_a(100)
    change_speed_b(100)

# Right
def Right():
    print('right')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)

    change_speed_a(100)
    change_speed_b(0)

# Left
def Left():
    print('left')
    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)

    change_speed_a(0)
    change_speed_b(100)

def Stop():
    print('stop')

    gpio.output(p_in1, True)
    gpio.output(p_in2, False)
    gpio.output(p_in3, True)
    gpio.output(p_in4, False)

    change_speed_a(0)
    change_speed_b(0)

def Right_soft():
    print('right soft')

    gpio.output(p_in1, False)
    gpio.output(p_in2, True)
    gpio.output(p_in3, False)
    gpio.output(p_in4, True)

init()
p_a = gpio.PWM(p_ena,100)
p_b = gpio.PWM(p_enb,100)

p_a.start(0)
p_b.start(0)

while True:
    command = input('Give input: ')
    
    if command == 'w':
        Forward()
    elif command == 'a':
        Left()
    elif command == 's':
        Backward()
    elif command == 'd':
        Right()
    elif command == 'f':
        Stop()
    elif command == 'l':
        speed_command = input('Give speed (0 - 100): ')
        change_speed_a(int(speed_command))
    elif command == 'p':
        speed_command = input('Give speed (0 - 100): ')
        change_speed_b(int(speed_command))
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