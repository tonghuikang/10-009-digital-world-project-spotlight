print("hello world")

from time import sleep
import RPi.GPIO as GPIO

pins = [17, 22, 13, 21]

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

def activate_led(pin_list, duty_list):
    pwm = [GPIO.PWM(item, 50) for item in pin_list]
    print("something")
    for i in range(len(pwm)):
#        try:
            pwm[i].start(duty_list[i] * 100)
            print("x")
#        except:
#            pass
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1.5)

while True:
#    try:
        activate_led(pins, [1, 0.9, 0.5, 1])
        activate_led(pins, [0.9, 0.8, 0.8, 1])
        activate_led(pins, [0.8, 0, 0.4, 0.8])
        activate_led(pins, [0.7, 0.6, 0.7, 0])
        activate_led(pins, [0.6, 0.5, 0, 1])
        activate_led(pins, [0, 0.4, 1, 0.9])
        activate_led(pins, [0.4, 0.3, 0.9, 1])
#    except KeyboardInterrupt:
#        print("keyboard interrupt")
#        break
#    except MemoryError:
#        pass

GPIO.cleanup()
print("GPIO cleanup completed")
