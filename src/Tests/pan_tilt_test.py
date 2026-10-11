from gpiozero import AngularServo 
from time import sleep    

# Creates a servo object on GPIO pin 17, telling gpiozero this servo can move
# from 0 to 180 degrees.
pan = AngularServo(17, min_angle = 0, max_angle = 180)  

# Same as above, but for GPIO pin 27
tilt = AngularServo(27, min_angle= 0, max_angle = 180)



input1 = input("Want to commence pan test?")
input1 = input.title()

if (input1 == 'Yes'):
    pan.angle = 90   # commands the pan servo to move to its leftmost position
    sleep(1)          # pauses the script for 1 second so you have time to see it move
    pan.angle = 180    # commands the pan servo to move back to center
    sleep(1)
    pan.angle = 90    # commands the pan servo to move to its rightmost position
    sleep(1)
    pan.angle = 0     # returns the pan servo to center before moving on

input2 = input("Want to commence tilt test?")
input2 = input.title()

if (input2 == "Yes"):
    tilt.angle = 90
    sleep(1)
    tilt.angle = 180  
    sleep(1)
    tilt.angle = 90   
    sleep(1)
    tilt.angle = 0    
    sleep(1)

    
pan.detach()   # stops sending a signal to the pan servo, so it stops holding position/torque
tilt.detach()  # same as above, for the tilt servo