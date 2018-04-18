# Spotlight project
F04 Group 2

Low Eng Hao (Dan) <BR>
Soh Jun Hern <BR>
Suryono Gunawan Ali <BR>
Tong Hui Kang <BR>
Wee Jian Hui Kevin <BR>
Yip Jun Han

# Assignment
> Define the problem you wish to solve in making a smart green housing and neighbourhood. <BR>
> Propose a solution to solve the problem and how the solution make use of the "smart"-ness of technology. The proposed solution must make use of GUI interface using Kivy. The proposed solution must make use of either Thymio or Raspberry-Pi or both. You can also make use all the components given in the starter kit for your prototype. The smartness of your solution should involve data analysis and prediction using regression and/or supervised classification (bonus point). <BR>
Research on proposed solutions and what components are needed. Check whether it can work with the existing platform given (either Thymio or Raspberry-Pi). <BR>
> Plan items to purchase besides those given in a starter kit. Each group is given a claimable budget of $50.

# Problem
Lights are often left switched on long after the users have left.
Even when users are in, having only a few users in a relatively large room equates to wastage.
In rooms with ample ambient lighting, the required intensity of indoor lighting can be reduced.

# Idea:
Use a camera to detect the presence and motion of personnel
General brightness of the room is analysed to determine effect of ambient lighting
Target's position is used to determine which lights should be switched on
Brightness of each light that is switched on is varied by room's general brightness and distance from target
Minimised usage in terms of number of active lights and brightness of each light reduces wastage of electricity
The brightness of each light can be modified based on user preferences via a GUI

# Characteristics
- Affordable design – Our camera is used for target acquisition and brightness analysis, both of which do not require high-resolution images. Hence, our choice of camera will reflect as such in our budget. 

- Smart design – When room users disagree with our programmed desired light settings, we receive feedback in the form of them manually toggling the brightness. These user data is recorded and analysed to recalibrate specific desired brightness by users of a particular room.

# Architecture
The code resides and runs on three Raspberry Pis (RPi), and communicates with a cloud MQTT server. One RPi receives camera input and identify the location of the individual and calculates instructions for the lights. Another RPi receives the instructions and controls the light. The last RPi allows the individual to remotely control his light preferences.

![alt text](https://i.imgur.com/hFjt2NX.png "Archi")

## Cloud Server
`./cloud_dw_1D/`
The cloud server hosts the communication between the user and the appliance. We preferred to use MQTT's publisher-subscriber system instead of FireBase because we require instant response between the user and the appliance.

Our server is hosted by Google Cloud Platform. The cloud runs on Ubuntu 16.04 and has an IP address assigned by Google Cloud. 

The folder contains sample code to test whether publishing and subscribing works.

## Camera
`./cam_dw_1D/`
This RPi is connected to an RPi camera. It identifies the location of the person from the image taken periodically. Then the RPi calculates which lights to light up at what intensity, taking into account of the user's preferences.

In our demonstration of the proof of concept, the person is represented by a green cap. OpenCV is used to detect and pinpoint the green cap in the picture - and this is a placeholder for a camera and code that is capable to work on humans and in the dark.

Meanwhile, the RPi sends usage data for the user to visualise his usage, and also possibly for an algorithm to train itself to optimise settings for the user.

## Lights
`./lights_dw_1D/`
Dismantled LED torchlights are used to represent the room lights that are to be adjusted based on the position of the user. As RPi pins are never meant for the powering of electronics, we used a motor driver as a relay to power the torchlights. The torchlights are powered by a set of four AAA batteries on a battery holder instead.

<div style="width:75%">![alt text](https://i.imgur.com/NvMlz3j.png "Lights")</div>

With the presence and position of the person, the lights close to the person will be lit up. The calculation is done on the camera nodes, this RPi executes the lighting instructions. We have a separate RPi for commanding the lights because taking the camera input is computationally intensive, and setting GPIO on PWN sometimes causes the Python script to terminate and it needs to be restarted without interfering with the camera.

## Kivy Interface
`./kivy_dw_1D/`
The user can adjust the brightness of individual lights based on his preferences, using a set of sliders corresponding to each light. The interface constantly subscribe to a copy of the instructions to the lights, and the brightness of the lights are displayed on the GUI. 

![alt text](https://i.imgur.com/PEAWeuD.png "Kivy")

When the settings are finalised, the app will send the adjustment preference over the cloud to the change the brightness of the lights. 

## Firebase
The Kivy interface needs to retain the slider settings previously set by the user after closing. On startup, the Kivy interface hence takes the slider settings from Firebase. Each time adjustment preferences are sent over the cloud, they are also sent to Firebase for long-term storage.

# How to run these
You need three RPi, one Linux-based cloud and a Firebase database. Clone this repository into all four locations.

On the cloud, set up the MQTT server according to this tutorial. You do not need to register a domain name, a static IP address is sufficient. https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04. Use the included test code to check whether the publishing and subscription works - which need not be run during demostration. The cloud has to be online at the stipulated IP address, however, to facilitate communications.

On the RPi with camera, connect an RPi camera. Run two Python scripts: 
`./cam_dw_1D/cam_calculate.py` for inetracting with the camera.
`./cam_dw_1D/adj_list_sub.py` for subsciption to `adj_list`, which updates `adj_list.txt` that is periodically read by `cam_calculate.py`

On the RPi with the lights, connect four lights. Drivers are recommended to avoid running large current through the RPi. You can use `./lights_dw_1D/lights_test.py` to test the lights. Run this python script:
`./lights_dw_1D/call.py` which runs `gpio_operator.py` and re-runs it terminates for any reason.

On the RPi meant for Kivy interface, run these Python script in order:
`./kivy_dw_1D/duty_list_sub.py` to subscribe to a copy of the instructions the lights are receiving for display.
`./kivy_dw_1D/interface.py` which is the kivy interface. It publishes to `adj_list` when the configurations are changed.

When you are done setting up with your own firebase, obtain the secret key from the Firebase and update the secret on `./cam_dw_1D/adj_list_sub.py` and `cam_dw_1D/cam_calculate.py`.

# Conclusion
With these we are able to help users can save energy wasted on lighting up areas that the individual is not using, thus helping to reduce carbon emissions.

