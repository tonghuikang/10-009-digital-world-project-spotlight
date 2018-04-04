# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import paho.mqtt.client as mqttClient
from tlkh_camera import PiVideoStream
from time import sleep

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

Connected = False

broker_address = "35.197.131.13"
port = 8883

client = mqttClient.Client("SomeDifferentName")
client.username_pw_set("sammy", password="password") #set usrnm and pwd
client.on_connect = on_connect #attach function to callback
client.connect(broker_address, port=port)

#client.publish("test2","something")

cv2.setUseOptimized(True)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

## if a video path was not supplied, grab the reference
## to the webcam
#if not args.get("video", False):
#    camera = cv2.VideoCapture(0)
#
## otherwise, grab a reference to the video file
#else:
#    camera = cv2.VideoCapture(args["video"])

# TODO: IMPLEMENT MQTT AND PUBLISH POSITIONS
camera = PiVideoStream().start()

import time
time.sleep(1.0)

# keep looping
while True:
    # grab the current frame
    frame = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

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
            
            general_brightness = np.sum(np.sum(hsv[:,:,2]))/345600.
            upload_string = "{},{},{:2f}".format(int(x),int(y),general_brightness)
            # print(Connected)
            print(upload_string)
            client.publish("test2",upload_string)
            sleep(5)
    
    # update the points queue
    pts.appendleft(center)
    
    #print("check")
    #client.publish("test2", "".join([str(x),",",str(y)]))
    #client.publish("test2", "something")
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
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
camera.stop()
