#10.009 The Digital World 1D Project
#17F04 Group 2

''' LIGHT OPERATION VIA GPIO'''
'''
This script receives duty_list from 
cam_calculate.py and activates the 
lights accordingly to produce the 
desired brightness level. 
'''
#==============================================================================

import paho.mqtt.client as mqttClient
from time import sleep
import RPi.GPIO as GPIO

pins = [17, 22, 13, 21]

GPIO.cleanup() #in case GPIO not cleaned before this
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)
pwm = [GPIO.PWM(item, 50) for item in pins]
for item in pwm:
    item.start(0)

#activate lights according to duty cycle assigned
def activate_led(duty_list):
    for i in range(len(pwm)):
        pwm[i].ChangeDutyCycle(duty_list[i]*100)
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1)

#activate lights upon receiving duty_list
def on_message(client, userdata, message):
    received_data = str(message.payload.decode("utf-8"))
    print("Message received:", received_data)
    received_data_split = received_data.split(',')
    duty_list = [float(item) for item in received_data_split]
    activate_led(duty_list)

#setting up connection to Google Cloud
broker_address="35.197.131.13"
port = 8883
print("Creating new instance")
dw1d = mqttClient.Client("DW1Dgpiosub")
dw1d.username_pw_set("sammy","password")  #set usernames and passwords
dw1d.on_message = on_message              #attach functions to callback
print("Connecting to broker")
dw1d.connect(broker_address, port=port)   #connect to broker

#actual loop for receiving info
dw1d.loop_start()
dw1d.subscribe("gpio_list")
sleep(100000)
dw1d.loop_stop()

GPIO.cleanup()
