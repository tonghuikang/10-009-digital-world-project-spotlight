#10.009 The Digital World 1D Project
#17F04 Group 2

''' CAMERA & LIGHT CALCULATION '''
'''
This script reads the adj_list from 
adj_list_sub.py and obtains the person's 
position and the room brightness from the 
camera. These parameters are then used to 
calculate the required duty cycle of each 
light and written as a string, duty_list. 
This string is then published for activating 
the lights via gpio_operator.py and for 
displaying on the Kivy app via interface.py.

The initial adj_list is not published when 
the Kivy app is closed. To keep the lights 
running as desired, adj_list is initialised 
using the values on Firebase.
'''
#==============================================================================

'''============================================================================
                         Part I: Initialise program
============================================================================'''
import paho.mqtt.client as mqttClient
from collections import deque
import numpy as np
import argparse
import imutils
from tlkh_camera import PiVideoStream
import cv2
from time import sleep
from firebase import firebase

#set up Firebase
url = "https://dw2018-1d-project.firebaseio.com/"
secret = 'mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL'
fire = firebase.FirebaseApplication(url, secret)

#set up coordinate system for "person"
class Target:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return '({},{})'.format(self.x, self.y)

'''=================================================== Setting up the camera'''
cv2.setUseOptimized(True) #OpenCV

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

#define the lower and upper boundaries of the "green"
#ball in the HSV color space, then initialize the
#list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

camera = PiVideoStream().start()
sleep(1)

def get_obj_position_and_brightness():
    # grab the current frame
    frame = camera.read()

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    x,y = 0,0

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            general_brightness = float(np.sum(np.sum(hsv[:,:,2]))/345600.)
            sleep(0.1)
        
        # update the points queue
        pts.appendleft(center)
        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i+1)) * 2.5)
            cv2.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)

        # show the frame on screen
        #cv2.imshow("Frame", frame)
    
        person = Target(int(x), int(y))
        print('\nPerson is at {}; brightness is {:.2f}'.format(person, general_brightness))
        return person, general_brightness

'''============================================= Setting up the light system'''
#set up coordinate system for lights
class Light:
    def __init__(self, x, y, adj=1):
        self.x = x
        self.y = y
        self.adj = adj    #user preference of light's brightness (0-1)
        self.dist = 0     #distance from person
        self.duty = 100   #duty cycle varying with brightness

#set light coordinates
'''
@-----------------------+ 0      legend:
|#1         |         2#|        @ - origin
|           |           | 112    # - light
|           |           |        x - camera (600 by 450 px)
|-----------x-----------| 225
|           |           |
|           |           | 338
|#3         |         4#|
+-----------------------+ 450
0    150   300   450   600

Light no.  1   2   3   4          '''
light_x = [0, 600, 0, 600]   #coordinates following diagram above
light_y = [0,  0, 450,450]
init_adj_list = fire.get("/adj_list")
light_list = [Light(light_x[i], light_y[i], init_adj_list[i]) for i in range(4)]

'''======================================================= Reading text file'''
#directory of text file receiving adj_list data
txt = '/home/pi/thymio/cam_dw_1D/adj_list.txt'

def get_adj_list():
    f = open(txt, 'r')
    reading = f.readline()
    adj_list = [round(float(item),2) for item in reading.split(',')]
    f.close()
    return adj_list

'''============================================================================
                         Part II: Light Duty Calculation
============================================================================'''

#decide brightness of each light
def decide_brightness():
    #obtain person's position, brightness, adj_list
    person, brightness = get_obj_position_and_brightness()
    adj_list = get_adj_list()
    
    #alter base attribute of lights
    for i in range(len(light_list)):
        light_list[i].adj = float(adj_list[i])
    print('Adjustments: {}'.format(adj_list))
    
    #determine duty cycle of lights
    duty_str = ''
    for light in light_list:
        #alter dist attribute
        light.dist = ( (person.x - light.x)**2 + (person.y - light.y)**2 )**0.5
        #alter duty attribute
        power = (100 - brightness) * light.adj  #factoring user preference
        if light.dist < 376:
            mult = ( (376 - light.dist) / 376 )**0.25
            light.duty = power * mult
            duty_str += '{:.4f},'.format(light.duty / 100)
        else:
            light.duty = 0
            duty_str += '0,'
    duty_str = duty_str.rstrip(',') #remove extra comma
    
    #publish duty_list to Google Cloud
    print('Light duty (published): {}'.format(duty_str))
    dw1d.publish("duty_list", duty_str)
    dw1d.publish("gpio_list", duty_str)

'''============================================================================
           Part III: Actual Operation & Publishing to Google Cloud
============================================================================'''
def on_connect(client, userdata, flags, rc):
    if rc == 0:
         print("Connected to broker")
         global Connected
         Connected = True
    else:
         print("Connection failed")

#set up connection to Google Cloud
Connected = False
broker_address="35.197.131.13"
port = 8883
print("Creating new instance")
dw1d = mqttClient.Client("DW1Ddutypub")
dw1d.username_pw_set("sammy","password")  #set usernames and passwords
dw1d.on_connect = on_connect
print("Connecting to broker")
dw1d.connect(broker_address, port=port)   #connect to broker

while True:
    try:
        decide_brightness()
    except KeyboardInterrupt:
        break
    except:
        sleep(0.1)

cv2.destroyAllWindows()
camera.stop()
