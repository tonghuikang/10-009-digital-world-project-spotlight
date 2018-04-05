#10.009 The Digital World 1D Project
#17F04 Group 2
'''#########################
# Part I: Initialise program
############################'''
import paho.mqtt.client as mqtt #import the client1 for Google cloud
import time
#import RPi.GPIO as GPIO
from firebase import firebase

#set up Firebase
url = "https://dw2018-1d-project.firebaseio.com/"
secret = 'mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL'
fire = firebase.FirebaseApplication(url, secret)

#set up coordinate system
class Target:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return '({},{})'.format(self.x, self.y)

class LED_coord:
    def __init__(self, x, y, pin, base = 0.8):
        self.x = x
        self.y = y
        self.pin = pin
        self.base = base     #base power setting (range 0-1) varying with user preference
        self.dist = 0.       #distance from person
        self.duty = 100      #duty cycle varying with brightness
    def __str__(self):
        return 'LED ({},{}), GPIO pin {}'.format(self.x, self.y, self.pin)

'''    LAYOUT:
O-------------------+ 0
|   |   |   |   |   |
|--1#--2#--3#--4#---| 112
|   |   |   |   |   |
|--5#--6#-x7#--8#---| 225
|   |   |   |   |   |
|--9#-10#-11#-12#---| 338
|   |   |   |   |   |
+-------------------+ 450
0  120 240 360 480 600
Legend
# - LED
x - camera (resolution 600 x 450)
O - Origin (0,0) is top left        '''

p1 = LED_coord(120,112,19)    #LED coordinates
p2 = LED_coord(240,112,5)
p3 = LED_coord(360,112,13)
p4 = LED_coord(480,112,26)
p5 = LED_coord(120,225,12)
p6 = LED_coord(240,225,21)
p7 = LED_coord(360,225,20)
p8 = LED_coord(480,225,16)
p9 = LED_coord(120,338,6)
p10 = LED_coord(240,338,7)
p11 = LED_coord(360,338,8)
p12 = LED_coord(480,338,9)
led_list = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]

'''#########################
# Part II: Data Manipulation 
############################'''

'''Step 1: read data from Google Cloud (string: "x,y,brightness")'''
def get_obj_position_and_brightness(received_data):
    data = received_data.split(',')
    brightness = float(data[2])
    person = Target(int(data[0]), int(data[1]))
    print('Person is at {}; brightness is {}'.format(person, brightness))
    return person, brightness

'''Step 2: decide brightness of each LED'''
def decide_brightness(person, brightness):
    #alter base attribute of LEDs
    adj_list = fire.get('/adj_list')
    for i in range(len(led_list)):
        led_list[i].base = adj_list[i]
    #for debugging=============================================================
    check_base = [led.base for led in led_list]
    print('LED adjustments: {}'.format(check_base))
    #==========================================================================
    
    #determine duty cycle of LEDs
    for led in led_list:
        #alter dist attribute
        led.dist = ( (person.x - led.x)**2 + (person.y - led.y)**2 )**0.5
        #alter duty attribute
        power1 = (100 - brightness) * led.base  #factoring base
        if led.dist < 165:    #------------------LED is at most diagonally adjacent
            mult = ( (165 - led.dist) / 165 )**0.33
            led.duty = power1 * mult
        else:    #-------------------------------LED is too far away, do not use
            led.duty = 0
    #for Firebase and debugging================================================
    check_duty = [led.duty for led in led_list]
    print('LED duty cycles: {}'.format(check_duty))
    fire.put('/', 'led_used', check_duty)
    #==========================================================================

'''Step 3: activate LEDs according to duty cycle assigned'''
def activate_led():
    GPIO.setmode(GPIO.BCM)
    print('Activating LEDs')
    for led in led_list:
        GPIO.setup(led.pin, GPIO.OUT)
        pwm_led = GPIO.PWM(led.pin, 50)
        pwm_led.start(100)
        pwm_led.ChangeDutyCycle(led.duty)
    GPIO.cleanup()

'''##################
# Part III: Operation
#####################'''
#main function that calls everything in Part II sequentially
def on_message(client, userdata, message):
    received_data = str(message.payload.decode("utf-8"))
    print("================================\nMessage received", received_data)
    person, brightness = get_obj_position_and_brightness(received_data)
    decide_brightness(person, brightness)
    #activate_led()

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