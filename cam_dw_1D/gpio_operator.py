#10.009 The Digital World 1D Project
#17F04 Group 2

''' LED OPERATION '''
'''
Read duty_list from "gpio_list" topic
Do GPIO stuff
'''
#==============================================================================

'''============================================================================
                         Part I: Initialise program
============================================================================'''
import paho.mqtt.client as mqttClient
from time import sleep
import RPi.GPIO as GPIO

pins = [5, 22, 27, 17]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

'''============================================================================
                           Part II: LED Operation
============================================================================'''
#activate LEDs according to duty cycle assigned
def activate_led(pins, duty_list):
    print("Activating LEDs")
    pwm = [GPIO.PWM(item, 50) for item in pins]
    for i in range(len(pwm)):
        pwm[i].start(duty_list[i] * 100)
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1)

#activate LEDs upon receiving duty_list
def on_message(client, userdata, message):
    received_data = str(message.payload.decode("utf-8"))
    print("Message received:", received_data)
    received_data_split = received_data.split(',')
    duty_list = [float(item) for item in received_data_split]
    activate_led(pins, duty_list)

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
print("Subscribed, waiting for message")
dw1d.subscribe("gpio_list")
sleep(100)
dw1d.loop_stop()
print("Subscription ended")

GPIO.cleanup()
print("GPIO cleanup completed")