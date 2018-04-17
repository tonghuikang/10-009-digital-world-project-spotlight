# 4 LEDs only!

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
import RPi.GPIO as GPIO

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
    #print(np.shape(hsv))
    #print(np.sum(np.sum(hsv[:,:,2])))
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
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        #cv2.imshow("Frame", frame)
    
        person = Target(int(x), int(y))
        print('\nPerson is at {}; brightness is {:.2f}'.format(person, general_brightness))
        return person, general_brightness

'''============================================== Setting up the LED control'''
#set up coordinate system for LEDs
class LED_coord:
    def __init__(self, x, y, pin, userpref=0.8):
        self.x = x
        self.y = y
        self.pin = pin           #GPIO pin number
        self.userpref = userpref #user preference of LED's brightness (0-1)
        self.dist = 0.           #distance from person
        self.duty = 100          #duty cycle varying with brightness
    def __str__(self):
        return 'LED ({},{}), GPIO pin {}'.format(self.x, self.y, self.pin)

#set LED coordinates
'''
@-------------------+ 0     legend:
|   |   |   |   |   |       @ - origin
|--1#--2#--3#--4#---| 112   # - LED
|   |   |   |   |   |       x - camera (600 x 450 px)
|--5#--6#-x7#--8#---| 225
|   |   |   |   |   |
|--9#-10#-11#-12#---| 338
|   |   |   |   |   |
+-------------------+ 450
0  120 240 360 480 600
       
LED no.    1   2   3   4   5   6   7   8   9   10  11  12'''
led_x =   [120,240,360,480]
led_y =   [112,112,112,112]
led_pin = [5,  22, 27, 17]
led_list = [LED_coord(led_x[i],led_y[i],led_pin[i]) for i in range(4)]

'''======================================================= Reading text file'''
#directory of text file receiving adj_list data
txt = '/home/pi/Desktop/adjlist.txt'

def get_adj_list():
    f = open(txt, 'r')
    reading = f.readline()
    adj_list = [round(float(item),2) for item in reading.split(',')]
    f.close()
    return adj_list

'''============================================================================
                           Part II: LED Operation
============================================================================'''

#decide brightness of each LED
def decide_brightness():
    #obtain person's position, brightness, adj_list
    person, brightness = get_obj_position_and_brightness()
    adj_list = get_adj_list()
    
    #alter base attribute of LEDs
    for i in range(len(led_list)):
        led_list[i].userpref = float(adj_list[i])
    print('Adjustments: {}'.format(adj_list))
    
    #determine duty cycle of LEDs
    duty_str = ''
    for led in led_list:
        #alter dist attribute
        led.dist = ( (person.x - led.x)**2 + (person.y - led.y)**2 )**0.5
        #alter duty attribute
        power1 = (100 - brightness) * led.userpref  #factoring user pref
        if led.dist < 165:    #--------------LED is at most diagonally adjacent
            mult = ( (165 - led.dist) / 165 )**0.25
            led.duty = power1 * mult
            duty_str += '{:.4f},'.format(led.duty / 100)
        else:    #---------------------------LED is too far away, do not use
            led.duty = 0
            duty_str += '0,'
    duty_str = duty_str.rstrip(',') #remove extra comma
    
    #publish duty_list to Google Cloud
    print('LED duty (not published): {}'.format(duty_str))
    #dw1d.publish("duty_list", duty_str)

#activate LEDs according to duty cycle assigned
def activate_led():
    print('Activating LEDs')
    for led in led_list:   
        pwm_led = GPIO.PWM(led.pin, 50)
        pwm_led.start(led.duty)
    sleep(1)

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

def exit_cleanup():
    cv2.destroyAllWindows()
    camera.stop()
    GPIO.cleanup()

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

#set up GPIO
GPIO.setmode(GPIO.BOARD)
for pin in led_pin:
    GPIO.setup(pin, GPIO.OUT)

while True:
    try:
        decide_brightness()
        activate_led()
    except KeyboardInterrupt:
        exit_cleanup()
    except:
        sleep(0.1)