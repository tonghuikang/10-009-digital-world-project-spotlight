import subprocess
import os
from time import sleep

sleep(10)

while True:
    try:
        os.system('python /home/pi/thymio/lights_dw_1D/startup.py')
    except:
        pass
