# Spotlight project


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
Sustainable design – When our IR camera does not detect any changes to our target’s position, our VIS camera will not be switched on. Similarly, our IR camera itself will not be actuated perpetually, but on a 1:10 work-rest-cycle. 
Affordable design – Our IR and VIS cameras are used for target acquisition and brightness analysis, both of which do not require high resolution images. Hence, our choice of camera will reflect as such in our budget. 
Smart design – When room users disagree with our programmed desired light settings, we receive feedback in the form of them manually toggling the brightness. This user data is recorded and analysed to recalibrate a specific desired brightness by users of a particular room. 

# Hardware Architecture
The code exist on three places. One on the cloud, one of each RPi. 

TODO: Comms chart

## Cloud Server
The cloud server hosts communication between the user and the applicance. We preferred to use a publisher-subscriber instead of firebase because we require instant response between the user and the appliance.

Our cloud is hosted by Google Cloud Platform. The cloud is on Ubuntu 16.04 and has a IP address assigned by Google Cloud. 
The code that the cloud runs on is inside `cloud_dw_1D`.

We followed this tutorial to set up a mqtt server (https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04).

## Camera and lights
The camera serves to identify the presence and location of the person. With the existance and position of the person, lights close to the person will be light up, based on users' perferences.

In our demostration of the proof of concept, the person is represented by the Thymio robot with a green cap. OpenCV is used to detects and pinpoint a green cap on the Thymio - and this is a placeholder for a camera and code that is capable to work on humans and in the dark. Breadboard LED lights are used to represent the room lights that is to be adjusted based on the postion of the user.

Meanwhile, the RPi sends usage data for the user to visualise his usage, and also possibly for an algorithm to train itself to optimise settings for the user.

## Adjustment node
The user can adjust the brightness of individual lights based on his preference. 
In our demostration, the user can adjust the brightness of each individual lights using our inferface. 


