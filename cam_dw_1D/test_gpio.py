from time import sleep
import RPi.GPIO as GPIO

pins = [21, 5, 13]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

#activate LEDs according to duty cycle assigned
def activate_led(duty_list):
    print("Activating LEDs")
    for i in range(len(pins)):
        pwm_led = GPIO.PWM(pins[i], 50)
        pwm_led.start(duty_list[i] * 100)
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1)

activate_led([1, 0.9, 0.5])
activate_led([0.9, 0.8, 0.8])
activate_led([0.8, 0, 0.4])
activate_led([0.7, 0.6, 0.7])
activate_led([0.6, 0.5, 0])
activate_led([0, 0.4, 1])
activate_led([0.4, 0.3, 0.9])

GPIO.cleanup()
print("GPIO cleanup completed")