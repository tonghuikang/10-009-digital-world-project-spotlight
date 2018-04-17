from time import sleep
import RPi.GPIO as GPIO

pins = [21]

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

#activate LEDs according to duty cycle assigned
def activate_led(duty_list):
    print("Activating LEDs")
    for i in range(len(pins)):
        pwm_led = GPIO.PWM(pins[i], 50)
        pwm_led.start(duty_list[i] * 100)
    print("LEDs activated accordingly")
    sleep(1)

activate_led([1])
activate_led([0.9])
activate_led([0.8])
activate_led([0.7])
activate_led([0.5])

GPIO.cleanup()
print("GPIO cleanup completed")