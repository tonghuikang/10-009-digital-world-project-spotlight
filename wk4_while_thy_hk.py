from pythymiodw import *
from time import sleep
from firebase import firebase

url = "https://dw-1d-week-4-3af73.firebaseio.com/" # URL to Firebase database
token = 'Lqv3YbIogV3o3Q7sAEnotO3Ld0WKzUtjOp1jiSoJ' # unique token used for authentication

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto
# the database and also retrieve data from the database.
firebase = firebase.FirebaseApplication(url, token)

robot = ThymioReal() # create an eBot object

# Write the code to control the eBot here
def left():
    robot.wheels(-100, 100)
    sleep(1)
    robot.wheels(0,0)
    sleep(1)

def right():
    robot.wheels(100, -100)
    sleep(1)
    robot.wheels(0,0)
    sleep(1)

def forward():
    robot.wheels(100, 100)
    sleep(1)
    robot.wheels(0,0)
    sleep(1)

while True:
    no_movements = True

    while no_movements:
        # Check the value of movement_list in the database at an interval of 0.5
        # seconds. Continue checking as long as the movement_list is not in the
        # database (ie. it is None). If movement_list is a valid list, the program
        # exits the while loop and controls the eBot to perform the movements
        # specified in the movement_list in sequential order. Each movement in the
        # list lasts exactly 1 second.
    
        # Write your code here
        sleep(0.5)
        movement_list = firebase.get('/movement_list')
        if len(movement_list) > 0:
            print(movement_list)
            break

    # 'up' movement => robot.wheels(100, 100)
    # 'left' movement => robot.wheels(-100, 100)
    # 'right' movement => robot.wheels(100, -100)
    for i in movement_list:
        if i == 'l':
            left()
        elif i == 'r':
            right()
        elif i == 'f':
            forward()
    firebase.put('/','movement_list','') # might as well overwrite sua
