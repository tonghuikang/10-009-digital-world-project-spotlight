from RPi import GPIO
from firebase import firebase

url = "https://dw-1d-week-4-3af73.firebaseio.com/" # URL to Firebase database
token = "Lqv3YbIogV3o3Q7sAEnotO3Ld0WKzUtjOp1jiSoJ" # unique token used for authentication

firebase=firebase.FirebaseApplication(url,token)

GPIO.setmode(GPIO.BCM)
ledcolor={'yellow':20, 'red':21}

GPIO.setup(ledcolor.values(), GPIO.OUT)

# =============================================================================
# def set_led(ledno, status):
#     if ledno == 20 and GPIO
# =============================================================================


while True:
    if firebase.get("/red_led_status") == "down":
        GPIO.output(21, GPIO.high)
    elif firebase.get("/red_led_status") == "normal":
        GPIO.output(21, GPIO.low)
    if firebase.get("/yellow_led_status") == "down":
        GPIO.output(20, GPIO.high)
    elif firebase.get("/yellow_led_status") == "normal":
        GPIO.output(20, GPIO.low)