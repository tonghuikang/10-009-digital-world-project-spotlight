import RPi.GPIO as GPIO
from time import sleep
from firebase import firebase

url = 'https://reptilians-c17d7.firebaseio.com' # URL to Firebase database
token = 'I3UGIj9H5p6FyphVFheoJh0Wr5orVoOe4XetLzWQ' # unique token used for authentication

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto 
# the database and also retrieve data from the database.
firebase = firebase.FirebaseApplication(url, token)
print("est. comms. firebase")

# Use the BCM GPIO numbers as the numbering scheme.
GPIO.setmode(GPIO.BCM)

# Use GPIO 12, 16, 20 and 21 for the buttons.
buttons = [12, 16, 20, 21] ##

# Set GPIO numbers in the list: [12, 16, 20, 21] as input with pull-down resistor.
GPIO.setup(buttons, GPIO.IN, GPIO.PUD_DOWN)  # ref hk_edit.py

# Keep a list of the expected movements that the eBot should perform sequentially.
movement_list = ''

#cooldowntime = 0.5 # in seconds
done = False
released = False

print("listening to buttons")

while not done:
    released = False
    if GPIO.input(buttons[0]) == GPIO.HIGH:
        while not released:
            if GPIO.input(buttons[0]) == GPIO.LOW:
                released = True
        movement_list += '0'
        print("0")
    if GPIO.input(buttons[1]) == GPIO.HIGH:
        while not released:
            if GPIO.input(buttons[1]) == GPIO.LOW:
                released = True
        movement_list += '1'
        print("1")
    if GPIO.input(buttons[2]) == GPIO.HIGH:
        while not released:
            if GPIO.input(buttons[2]) == GPIO.LOW:
                released = True
        movement_list += '2'
        print("2")
    if GPIO.input(buttons[3]) == GPIO.HIGH:
        while not released:
            if GPIO.input(buttons[3]) == GPIO.LOW:
                released = True
        movement_list += '3'
        done = True
        print("3")
    # Write your code here

print(movement_list)
    '''
    We loop through the key (button name), value (gpio number) pair of the buttons
    dictionary and check whether the button at the corresponding GPIO is being
    pressed. When the OK button is pressed, we will exit the while loop and 
    write the list of movements (movement_list) to the database. Any other button
    press would be stored in the movement_list.

    Since there may be debouncing issue due to the mechanical nature of the buttons,
    we can address it by putting a short delay between each iteration after a key
    press has been detected.
    '''
#    pass

print("while loop done")
# Write to database once the OK button is pressed
firebase.put('/', 'lst', movement_list) # put the value True into node lazy
print("ending code")
