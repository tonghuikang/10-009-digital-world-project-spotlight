from time import sleep
import RPi.GPIO as GPIO

pins = [17, 22, 13, 21]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

#activate LEDs according to duty cycle assigned
def activate_led(pins, duty_list):
    print("Activating LEDs")
    for i in range(len(pins)):
        pwm_led = GPIO.PWM(pins[i], 50)
        pwm_led.start(duty_list[i] * 100)
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1)

activate_led(pins, [1, 0.9, 0.5, 1])
activate_led(pins, [0.9, 0.8, 0.8, 1])
activate_led(pins, [0.8, 0, 0.4, 0.8])
activate_led(pins, [0.7, 0.6, 0.7, 0])
activate_led(pins, [0.6, 0.5, 0, 1])
activate_led(pins, [0, 0.4, 1, 0.9])
activate_led(pins, [0.4, 0.3, 0.9, 1])

GPIO.cleanup()
print("GPIO cleanup completed")