#10.009 The Digital World 1D Project
#17F04 Group 2
'''#########################
# Part I: Initialise program
############################'''
from math import sqrt
import paho.mqtt.client as mqtt #import the client1 for Google cloud
import time
import RPi.GPIO as GPIO
from firebase import firebase

#set up Firebase
url = "https://dw2018-1d-project.firebaseio.com/"
secret = 'mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL'
fire = firebase.FirebaseApplication(url, secret)

#set up coordinate system (0-255)
class Coordinate:
    def __init__(self, x=0 , y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return '({},{})'.format(self.x,self.y)

class LED_coord:
    def __init__(self, x, y, pin):
        self.x = x
        self.y = y
        self.pin = pin
    def __str__(self):
        return 'LED ({},{}), GPIO pin {}'.format(self.x,self.y,self.pin)
'''
O---------------+ 0
| p1| p2| p3|   |
|---#---#---#---| 63
| p4|   | p5|   |
|---#---x---#---| 127
| p6| p7| p8|   |
|---#---#---#---| 191
|   |   |   |   |
+---------------+ 255
0  63  127 191 255
Legend
# - LED
x - camera
O - Origin (0,0) is top left
'''
#coordinates of the LEDS from 0-255 board
p1 = LED_coord(112,75,19)   #top left
p2 = LED_coord(112,150,5)   #top mid
p3 = LED_coord(112,225,13)  #top right
p4 = LED_coord(225,75,26)  #mid left
p5 = LED_coord(225,225,12) #mid right
p6 = LED_coord(337,75,21)  #bottom left
p7 = LED_coord(337,150,20) #bottom mid
p8 = LED_coord(337,225,16) #bottom right
led_list = [p1,p2,p3,p4,p5,p6,p7,p8]

'''#########################
# Part II: Data Manipulation 
############################'''

#analyse input from Google Cloud - 'x,y,b'
def get_object_position_and_brightness(received_data):
    data = received_data.split(',')
    brightness = float(data[2])
    person = Coordinate(int(data[0]),int(data[1]))
    print('Person is at {}'.format(person))
    return person, brightness

#compare person coord with LED coord to get the LEDs within range
def choose_led(person):
    distances = []
    led_used = [0,0,0,0,0,0,0,0]
    for led in led_list:
        distance = sqrt((person.x - led.x)**2 + (person.y - led.y)**2)
        if distance <= 270:
            distances.append((led,distance))
            led_used[led_list.index(led)] = 1
            print('Chose {}, {} from person'.format(led,round(distance,1)))
    fire.put('/','led_used',led_used)
    print('LED usage sent to Firebase')
    return distances    #output: [  (  LED , dist from person   )   ]

#take some input list, return output list normalised to limit
def normalise(lst, limit=100.0):
    ans = []
    try:
        for i in lst:
            lower, upper = min(lst), max(lst)
            ans.append( (i-lower) / (upper-lower) * limit/2 + limit/2)
    except ZeroDivisionError:
        ans.append(limit)
    return ans

#take list of LEDs with distances from person
def brightness_splitting(brightness, distances):
    top_up = 100 - brightness #how much extra light is needed from the LEDs
    fire.put('/','top_up',top_up) #upload top_up value to Firebase
    print('Top up needed: {} (sent to Firebase)'.format(top_up))
    led_flicker_raw = []
    for led in distances: #LEDs nearer to the person should be brightest
        try:
            required_power = top_up / led[1]**2
        except ZeroDivisionError:
            required_power = top_up / 0.0001
        led_flicker_raw.append(required_power)
    led_flicker = normalise(led_flicker_raw, top_up)
    return led_flicker

# now, tell each LED to light up w a duty cycle = required_power
def activate_led(distances, led_flicker):
    led_pins = [item[0].pin for item in distances]
    print('=====\nActivate',led)
    GPIO.setmode(GPIO.BCM)
    for i in led_pins:
        GPIO.setup(i, GPIO.OUT)
    for i in range(len(led_pins)):
        pwm_led = GPIO.PWM(led_pins[i],50)
        pwm_led.start(100) # test if we can combine this and ChangeDutyCycle
        duty = led_flicker[i]
        print('Duty of pin {}: {}'.format(led_pins[i],round(duty,1)))
        pwm_led.ChangeDutyCycle(duty)
    time.sleep(5)
    GPIO.cleanup()

'''##################
# Part III: Operation
#####################'''
### Google Cloud stuff ###
def on_message(client, userdata, message):
    received_data = str(message.payload.decode("utf-8"))
    print("======================\nMessage received ", received_data)
    person, brightness = get_object_position_and_brightness(received_data)
    distances = choose_led(person)
    led_flicker = brightness_splitting(brightness, distances)
    #activate_led(distances, led_flicker)

#setting up connection to Google Cloud
broker_address="35.197.131.13"
port = 8883
print("Creating new instance")
client = mqtt.Client("random") #create new instance
client.username_pw_set("sammy","password")
client.on_message=on_message #attach function to callback
print("Connecting to broker")
client.connect(broker_address, port=port) #connect to broker

#actual loop for receiving info
client.loop_start()
client.subscribe("test2")
time.sleep(100) #run loop for 100s, need to find out how to let it run forever
client.loop_stop()
GPIO.cleanup()
