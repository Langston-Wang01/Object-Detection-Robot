from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep    

pigoioFactory = PiGPIOFactory()

pan = AngularServo(17, initial_angle = 90, min_angle = 0, max_angle = 180, min_pulse_width =0.0005, max_pulse_width =0.0025, pin_factory = pigoioFactory)
tilt = AngularServo(27, initial_angle = 90, min_angle = 0, max_angle = 180, min_pulse_width =0.0005, max_pulse_width =0.0025, pin_factory = pigoioFactory)




input1 = input("Want to commence pan test?")
input1 = input1.title()

if (input1 == 'Yes'):
    pan.angle = 90
    sleep(1)
    pan.angle = 180
    sleep(1)
    pan.angle = 90
    sleep(1)
    pan.angle = 0

input2 = input("Want to commence tilt test?")
input2 = input2.title()

if (input2 == "Yes"):
    tilt.angle = 90
    sleep(1)
    tilt.angle = 180  
    sleep(1)
    tilt.angle = 70   
    sleep(1)
    tilt.angle = 0    
    sleep(1)


pan.detach()
tilt.detach()