import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
 the_message=str(message.payload.decode("utf-8"))
 print("message received " ,the_message)
 print("message topic=",message.topic)
 print("message qos=",message.qos)
 print("message retain flag=",message.retain)
 file = open("test.txt","w")
  file.write(the_message)
  file.close()
  time.sleep(0.001)
########################################
broker_address="localhost"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.username_pw_set("sammy","password")
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
client.subscribe("write_text")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")
time.sleep(100) # wait
client.loop_stop() #stop the loop
