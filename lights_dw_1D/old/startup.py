print("hello world")

from time import sleep
import RPi.GPIO as GPIO

pins = [17, 22, 13, 21]

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

def activate_led(pin_list, duty_list):
    pwm = [GPIO.PWM(item, 50) for item in pin_list]
    for i in range(len(pwm)):
        try:
            pwm[i].start(duty_list[i] * 100)
        except:
            pass
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1.5)

while True:
    try:
        activate_led(pins, [1.0, 0.0, 0.5, 0.0])
        activate_led(pins, [0.0, 1.0, 0.0, 0.5])
        activate_led(pins, [0.5, 0.0, 1.0, 0.0])
        activate_led(pins, [0.0, 0.5, 0.0, 1.0])
    except KeyboardInterrupt:
        print("keyboard interrupt")
        break
    except MemoryError:
        pass

GPIO.cleanup()
print("GPIO cleanup completed")
