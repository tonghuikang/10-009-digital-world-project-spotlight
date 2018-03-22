import paho.mqtt.client as mqttClient
from time import sleep
# from camera import PiVideoStream

# this = sys.modules[__name__]

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

client = mqttClient.Client("Python")
client.username_pw_set("sammy", password="password") #set usrnm and pwd
client.on_connect = on_connect #attach function to callback
client.connect(broker_address, port=port)

for x in range(1000):
    client.publish("test2", x)
    sleep(0.001)
