# this code will write random numbers to a text file at periodic intervals

import numpy as np
import time

while True:
    file = open("test.txt","w")
    random_num = str(np.random.randn())
    print(random_num)
    file.write(random_num)
    file.close()
    time.sleep(0.001)


#import paho.mqtt.client as mqtt #import the client1
#import time
#############
#def on_message(client, userdata, message):
# print("message received " ,str(message.payload.decode("utf-8")))
# print("message topic=",message.topic)
# print("message qos=",message.qos)
# print("message retain flag=",message.retain)
#########################################
#broker_address="localhost"
##broker_address="iot.eclipse.org"
#print("creating new instance")
#client = mqtt.Client("P1") #create new instance
#client.username_pw_set("sammy","password")
#client.on_message=on_message #attach function to callback
#print("connecting to broker")
#client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop
#print("Subscribing to topic","house/bulbs/bulb1")
#client.subscribe("house/bulbs/bulb1")
#client.subscribe("loc")
#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","OFF")
#time.sleep(100) # wait
#client.loop_stop() #stop the loop
