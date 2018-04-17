import RPi.GPIO as GPIO
from time import sleep
import time
# Use the BCM GPIO numbers as the numbering scheme
GPIO.setmode(GPIO.BCM)

# Use GPIO23 for LED 1, GPIO24 for LED 2 and GPIO18 for switch
leds = [5,  22, 27, 17, 26, 19, 13, 6,  21, 20, 16, 12]
switch = 18

# Set the GPIO23 and GPIO24 as output.
for led in leds:
    GPIO.setup(led, GPIO.OUT)

# Set the GPIO18 as input with a pull-down resistor.
GPIO.setup(switch, GPIO.IN, GPIO.PUD_DOWN)

def blink(gpio_number, duration):
    print(gpio_number)
    GPIO.output(gpio_number, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(gpio_number, GPIO.HIGH)
    time.sleep(duration)
    '''This function takes in two input: gpio_number and duration. The
        gpio_number specifies the GPIO number which the LED (to be blinked) is
        connected to. The duration is the blink interval in seconds.'''

# Write your code here
#     pass

# while True:

while True:
    for led in leds:
        blink(led,1)
