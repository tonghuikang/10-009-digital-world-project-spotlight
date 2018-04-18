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
Research on propose solutions and what are the components needed. Check whether it can work with the existing platform given (either Thymio or Raspberry-Pi). <BR>
> Plan items to purchase besides those given in a starter kit. Each group is given a claimable budget of $50.

# Problem
Lights are often left switched long after the users have left.
Even when users are in, having only a few users in a relatively large room equates to wastage.
In rooms with ample ambient lighting, the intensity of indoor lighting needed can be reduced.

# Idea:
Use an infrared (IR) camera to detect heat signatures and a visible light (VIS) camera to detect the brightness of the room.
IR camera takes a thermal image every ten seconds
If two consecutive images show our target at the same position (within threshold), activate VIS camera
VIS camera takes one image
Brightness at our target’s position is analysed to determine effect of ambient lighting
Brightness of indoor lighting adjusted to minimise wastage
Deactivate VIS camera; repeat

# Characteristics
- Sustainable design – When our IR camera does not detect any changes to our target’s position, our VIS camera will not be switched on. Similarly, our IR camera itself will not be actuated perpetually, but on a 1:10 work-rest-cycle. 

- Affordable design – Our IR and VIS cameras are used for target acquisition and brightness analysis, both of which do not require high-resolution images. Hence, our choice of camera will reflect as such in our budget. 

- Smart design – When room users disagree with our programmed desired light settings, we receive feedback in the form of them manually toggling the brightness. These user data is recorded and analysed to recalibrate specific desired brightness by users of a particular room. 

# Architecture
The code resides and run on three Raspberry Pis (RPi), and communicates with a cloud MQTT server. One RPi receives camera input and identify the location of the individual and calculates instructions for the lights. Another RPi receives the instructions and controls the light. The last RPi allows the individual to remotely control his light preferences.

![alt text](https://i.imgur.com/hFjt2NX.png "Archi")

## Cloud Server
`./cloud_dw_1D/`
The cloud server hosts the communication between the user and the appliance. We preferred to use MQTT's publisher-subscriber system instead of FireBase because we require instant response between the user and the appliance.

Our server is hosted by Google Cloud Platform. The cloud runs on Ubuntu 16.04 and has an IP address assigned by Google Cloud. We followed this tutorial to set up an MQTT server (https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04). 

The folder contains sample code to test whether publishing and subscribing works.

## Camera
`./cam_dw_1D/`
This RPi is connected to an RPi camera. It identifies the location of the person from the image taken periodically. Then the RPi calculates which lights to light up at what intensity, taking into account of the user's preferences.

In our demonstration of the proof of concept, the person is represented by a green cap. OpenCV is used to detect and pinpoint the green cap in the picture - and this is a placeholder for a camera and code that is capable to work on humans and in the dark.

Meanwhile, the RPi sends usage data for the user to visualise his usage, and also possibly for an algorithm to train itself to optimise settings for the user.

## Lights
`./lights_dw_1D/`
Dismantled LED torchlights are used to represent the room lights that are to be adjusted based on the position of the user. As RPi pins are never meant for the powering of electronics, we used a motor driver as a relay to power the torchlights. The torchlights are powered by a set of four AAA batteries on a battery holder instead.

![alt text](https://i.imgur.com/NvMlz3j.png "Lights")

With the existence and position of the person, the lights close to the person will be light up. The calculation is done on the camera nodes, this RPi executes the lighting instructions. We have a separate RPi for commanding the lights because taking the camera input is computationally intensive, and setting GPIO on PWN sometimes causes the Python script to terminate and it needs to be restarted without interfering with the camera.

## Kivy Interface
`./kivy_dw_1D/`
The user can adjust the brightness of individual lights based on his preferences. When the settings are finalised, the app will send the adjustment preference over the cloud to the change the brightness of the lights. 

# Conclusion
With these we are able to help users can save energy wasted on lighting up areas that the individual is not using, thus helping to reduce carbon emissions.
