from pythymiodw import *
from time import sleep
from firebase import firebase

url = 'https://reptilians-c17d7.firebaseio.com' # URL to Firebase database
token = 'I3UGIj9H5p6FyphVFheoJh0Wr5orVoOe4XetLzWQ' # unique token used for authentication

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto 
# the database and also retrieve data from the database.
firebase = firebase.FirebaseApplication(url, token)
print("est. comms. firebase")

# pull code from fire_base
lst_ = "0123" # pull from firebase
print(lst_)
lst = list(lst)
print(lst)
print("executing")

robot = ThymioReal() # create an eBot object

no_movements = True

while no_movements:
    if lst[0] == '0':
        move_0(robot)
    if lst[0] == '1':
        move_1(robot)
    if lst[0] == '2':
        move_2(robot)
    if lst[0] == '3':
        no_movements = False
    del movements[0] = # pop the first entry

    # Check the value of movement_list in the database at an interval of 0.5
    # seconds. Continue checking as long as the movement_list is not in the
    # database (ie. it is None). If movement_list is a valid list, the program
    # exits the while loop and controls the eBot to perform the movements
    # specified in the movement_list in sequential order. Each movement in the
    # list lasts exactly 1 second.

    # Write your code here

def move_0(robot): # passing robot as an object
    robot.wheels(100, 100) # make the robot move at same speed on both wheels
    robot.sleep(1) # wait for 5 seconds
    robot.wheels(0, 0)

def move_1(robot):
    robot.wheels(-100, 100) # make the robot move at same speed on both wheels
    robot.sleep(1) # wait for 5 seconds
    robot.wheels(0, 0)

def move_2(robot):
    robot.wheels(100, -100) # make the robot move at same speed on both wheels
    robot.sleep(1) # wait for 5 seconds
    robot.wheels(0, 0)

# Write the code to control the eBot here

# 'up' movement => robot.wheels(100, 100)
# 'left' movement => robot.wheels(-100, 100)
# 'right' movement => robot.wheels(100, -100)

