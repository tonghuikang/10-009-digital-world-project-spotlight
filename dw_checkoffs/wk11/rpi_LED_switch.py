from RPi import GPIO
from firebase import firebase

url = "https://dw-1d-week-4-3af73.firebaseio.com/" # URL to Firebase database
token = "Lqv3YbIogV3o3Q7sAEnotO3Ld0WKzUtjOp1jiSoJ" # unique token used for authentication

firebase=firebase.FirebaseApplication(url,token)

GPIO.setmode(GPIO.BCM)
ledcolor={'yellow':20, 'red':21}

GPIO.setup([20, 21], GPIO.OUT)

# =============================================================================
# def set_led(ledno, status):
#     if ledno == 20 and GPIO
# =============================================================================


while True:
    if firebase.get("/red_led_status") == "down":
        print(20)
        GPIO.output(21, GPIO.HIGH)
    elif firebase.get("/red_led_status") == "normal":
        print(30)
        GPIO.output(21, GPIO.LOW)
    if firebase.get("/yellow_led_status") == "down":
        print(40)
        GPIO.output(20, GPIO.HIGH)
    elif firebase.get("/yellow_led_status") == "normal":
        GPIO.output(20, GPIO.LOW)
        print(50)
