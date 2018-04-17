from time import sleep
import RPi.GPIO as GPIO

pins = [17, 22, 13, 21]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

def activate_led(pin_list, duty_list):
    pwm = [GPIO.PWM(item, 50) for item in pin_list]
    for i in range(len(pwm)):
        pwm[i].start(duty_list[i] * 100)
    print("LEDs activated accordingly: {}".format(duty_list))
    sleep(1.5)

dut = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
duty_test = []
for i in range(len(dut)):
    duty_test.append([dut[i], dut[-(i+1)], dut[i], dut[-(i+1)]])

for i in range(len(duty_test)):
    activate_led(pins, duty_test[i])

pwm = [GPIO.PWM(item, 50) for item in pins]
pwm.stop()
GPIO.cleanup()
print("GPIO cleanup completed")