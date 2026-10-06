from gpiozero import AngularServo 
from time import sleep    

# USED CLAUDE to help generate a quick test to check servo motors



# Creates a servo object on GPIO pin 17, telling gpiozero this servo can move
# from -90 to 90 degrees.
pan = AngularServo(17, min_angle=-90, max_angle=90)  

# Same as above, but for GPIO pin 27
tilt = AngularServo(27, min_angle=-90, max_angle=90)

pan.angle = -90   # commands the pan servo to move to its leftmost position
sleep(1)          # pauses the script for 1 second so you have time to see it move
pan.angle = 0     # commands the pan servo to move back to center
sleep(1)
pan.angle = 90    # commands the pan servo to move to its rightmost position
sleep(1)
pan.angle = 0     # returns the pan servo to center before moving on

tilt.angle = -90 
sleep(1)
tilt.angle = 0  
sleep(1)
tilt.angle = 90   
sleep(1)
tilt.angle = 0    

sleep(1)
pan.detach()   # stops sending a signal to the pan servo, so it stops holding position/torque
tilt.detach()  # same as above, for the tilt servo