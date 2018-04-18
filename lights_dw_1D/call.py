import subprocess
import os
from time import sleep

sleep(2)

while True:
    try:
        os.system('python /home/pi/thymio/lights_dw_1D/gpio_operator.py')
    except:
        pass
