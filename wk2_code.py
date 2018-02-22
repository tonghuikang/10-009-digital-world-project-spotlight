#!/usr/bin/python
# -*- coding: utf-8 -*-

from pythymiodw import *


def print_temp(t_celcius):
    F= (t_celcius * 1.8 )+ 32
    print ("The temperature is " , F , "and", t_celcius , "fahrenheit and celcius respectively")
    """ calculate t_fahrenheit and print both
    """

def forward(robot,speed, duration):
    
    robot.wheels(speed, speed)
    robot.sleep(duration)
    robot.wheels (0,0)
    
    """ move both wheels for that duration, and stop
    """

robot = ThymioReal() # create an object

############### Start writing your code here ################ 
speed = int(input("What do you want the speed of the robot to be"))
duration = int(input("How long do you want to robot to move?"))
# Prompt user to enter speed and duration of movement
forward(robot,speed, duration)

# Move according to the specified speed and duration

# Read temperature in celcius from the sensor and print it
temp = robot.temperature()
print_temp(temp)
########################## end ############################## 

robot.quit() # disconnect the communication

