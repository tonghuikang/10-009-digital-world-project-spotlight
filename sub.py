import paho.mqtt.client as mqtt #import the client1
import time


broker_address="localhost"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("PX") #create new instance
print("connecting to broker")
client.username_pw_set("sammy",password="password")
client.connect(broker_address) #connect to broker
#print("Subscribing to topic"," test2")
#client.subscribe("test2")
#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","OFF")
client.loop_start() #start the loop
print("Subscribing to topic","test2")
client.subscribe("test2")
#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","OFF")
time.sleep(100) # wait
client.loop_stop() #stop the loop
