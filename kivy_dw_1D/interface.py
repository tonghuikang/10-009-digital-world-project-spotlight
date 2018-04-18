#10.009 The Digital World 1D Project
#17F04 Group 2

''' KIVY APP SCRIPT '''
'''
This script takes in the duty list from the 
duty_list_sub.py subscriber script, and runs the Kivy App.
The Kivy App displays usage statistics, and 
allows user input to manually adjust lighting levels.
The input is then published from interface.py to 
adjust the actual lighting levels.
'''
#==============================================================================

'''============================================================================
                         Part I: Initialise program
============================================================================'''
from kivy.app import App

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager

from kivy.clock import Clock
from kivy.lang import Builder

from firebase import firebase
import paho.mqtt.client as mqtt

# set up Firebase
url = "https://dw2018-1d-project.firebaseio.com/"
secret = "mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL"
fire = firebase.FirebaseApplication(url, secret)

# set dimensions of GUI to the RPi monitor size
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

'''============================================================================
                         Part II: Kivy Builder
============================================================================'''
Builder.load_string("""
                    
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
<Screener>
    transition: FadeTransition()
    Screen: 
        name: "welcome"
        Button:
            text: "welcome"
            on_press: root.current = "main"
            on_press: root.set_adj_val() # triggers set_adj_val() to get initial values from 
                                         # Firebase and set as initial slider values
            on_press: root.start_stop()  # triggers my_callback() every second
    Screen:
        name: "main"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 2
                orientation: "horizontal"
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    ImageButton:
                        id: b0
                        source: "light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_0"
                    ImageButton:
                        id: b2
                        source: "light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_2"

                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    ImageButton:
                        id: b1
                        source: "light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_1"
                    ImageButton:
                        id: b3
                        source: "light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_3"
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Label:
                    id: blank_stat
                Label:
                    id: blank_stat_2
                Label:
                    id: blank_stat_3
                Label:
                    id: rt_globstat1_l00
                    text: ""
                Button:
                    text: "Quit"
                    padding: [400, 400]
                    on_press: root.on_stop()
                    
    Screen:
        name: "adj_0"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 2
                orientation: "horizontal"
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Image:
                        id: i0
                        source: "light.png"
                        color: [1,1,1,1]                      
                    Label:
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    id: s0
                    on_value: root.s0_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l0
                    text: "Adjustment: {}%".format(round(s0.value * 100,2))
                Label:
                    id: rt_localstat2_l0
                    text: ""
                Label:
                    id: rt_globstat1_l0
                    text: ""
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
    
    Screen:
        name: "adj_1"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Label:
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Image:
                        id: i1
                        source: "light.png"
                        color: [1,1,1,1]
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    id: s1
                    on_value: root.s1_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l1
                    text: "Adjustment: {}%".format(round(s1.value * 100,2))
                Label:
                    id: rt_localstat2_l1
                    text: ""
                Label:
                    id: rt_globstat1_l1
                    text: ""
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_2"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Image:
                        id: i2
                        source: "light.png"
                        color: [1,1,1,1]
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    id: s2
                    on_value: root.s2_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l2
                    text: "Adjustment: {}%".format(round(s2.value * 100,2))
                Label:
                    id: rt_localstat2_l2
                    text: ""
                Label:
                    id: rt_globstat1_l2
                    text: ""
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_3"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Label:
                BoxLayout:
                    rows: 2
                    orientation: "vertical"
                    Label:
                    Image:
                        id: i3
                        source: "light.png"
                        color: [1,1,1,1]
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    id: s3
                    on_value: root.s3_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l3
                    text: "Adjustment: {}%".format(round(s3.value * 100,2))
                Label:
                    id: rt_localstat2_l3
                    text: ""
                Label:
                    id: rt_globstat1_l3
                    text: ""
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
""")

'''============================================================================
                Part III: Root Widget Class with Functions used
============================================================================'''
class Screener(ScreenManager):
    
    # get adj_list from Firebase and set initial slider values
    def set_adj_val(self):
        init_adj_list = fire.get("/adj_list")
        self.ids.s0.value  = init_adj_list[0]
        self.ids.s1.value  = init_adj_list[1]
        self.ids.s2.value  = init_adj_list[2]
        self.ids.s3.value  = init_adj_list[3]
        
    # call my_callback() every second
    def start_stop(self):
        Clock.schedule_interval(self.my_callback, 1)
        
    # updates brightness shown in GUI display every second
    def my_callback(self, dt):
        # brightness of lights is updated in real time via a text file
        # duty_list_sub.py subscribes to updates from cam_calculate.py
        txt_f = open("/home/pi/thymio/kivy_dw_1D/duty_list.txt", "r")
        line = txt_f.readline()
        txt_f.close()
        duty_val_raw = line.split(",")

        # normalize values 0-1 to values 0.1-1; so that the light indicative 
        # buttons are still visible on GUI even when lights are off
        # float_total calculates the total power usage of the set-up
        duty_val = []
        for val in duty_val_raw:
            new_val = float(val)*0.9 + 0.1
            duty_val.append(new_val)
        # divide by 4 to show average; multiply by 100 to convert to percentage
        float_total = (round(( sum([float(x) for x in duty_val_raw]) / 4 ) * 100, 2))
        
        # sets brightness of lights on GUI according to brightness of actual lights
        self.ids.b0.color   = [1,1,1, (duty_val[0])]
        self.ids.i0.color   = [1,1,1, (duty_val[0])]
        self.ids.b1.color   = [1,1,1, (duty_val[1])]
        self.ids.i1.color   = [1,1,1, (duty_val[1])]
        self.ids.b2.color   = [1,1,1, (duty_val[2])]
        self.ids.i2.color   = [1,1,1, (duty_val[2])]
        self.ids.b3.color   = [1,1,1, (duty_val[3])]
        self.ids.i3.color   = [1,1,1, (duty_val[3])]
        
        # updates current brightness of each light (local) being selected
        self.ids.rt_localstat2_l0.text   = "Current Power Usage: {}%".format(round(float(duty_val[0]) * 100,2))
        self.ids.rt_localstat2_l1.text   = "Current Power Usage: {}%".format(round(float(duty_val[1]) * 100,2))
        self.ids.rt_localstat2_l2.text   = "Current Power Usage: {}%".format(round(float(duty_val[2]) * 100,2))
        self.ids.rt_localstat2_l3.text   = "Current Power Usage: {}%".format(round(float(duty_val[3]) * 100,2))
        
        # updates total usage of the set-up (global) for all screens
        self.ids.rt_globstat1_l00.text = "Total Power Usage: {}%".format(float_total)
        self.ids.rt_globstat1_l0.text  = "Total Power Usage: {}%".format(float_total)
        self.ids.rt_globstat1_l1.text  = "Total Power Usage: {}%".format(float_total)
        self.ids.rt_globstat1_l2.text  = "Total Power Usage: {}%".format(float_total)
        self.ids.rt_globstat1_l3.text  = "Total Power Usage: {}%".format(float_total)
        
    # when "save settings" button is pushed, update adj_list according to slider values
    adj_list = [1, 1, 1, 1]
    def s0_func(self, *args):
        value = args[1]
        self.adj_list[0] = value
        
    def s1_func(self, *args):
        value = args[1]
        self.adj_list[1] = value
        
    def s2_func(self, *args):
        value = args[1]
        self.adj_list[2] = value
        
    def s3_func(self, *args):
        value = args[1]
        self.adj_list[3] = value
        
    # publish adj_list
    def send_adj_list(self):
        self.dw1d.publish("adj_list", str(self.adj_list).strip('[]'))
    
    # connect to Google Cloud, prior to publishing
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
             print("Connected to broker")
             global Connected
             Connected = True
        else:
             print("Connection failed")
    
    # setting up connection to Google Cloud
    Connected = False
    broker_address="35.197.131.13"
    port = 8883
    print("Creating new instance")
    dw1d = mqtt.Client("DW1Dadjpub")
    dw1d.username_pw_set("sammy","password")  #set usernames and passwords
    dw1d.on_connect = on_connect
    print("Connecting to broker")
    dw1d.connect(broker_address, port=port)   #connect to broker
    
    # cut the App and close the window
    def on_stop(self):
        App.get_running_app().stop()

# custom widget class for an image that has button properties such as on_press
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
    
    def on_press(self):
        pass

'''============================================================================
                Part IV: Instantiating and Running the App
============================================================================'''
# instantiating and building the App
class smart_lightingApp(App):
    def build(self):
        return Screener()

# run the App
if __name__ == "__main__":
    smart_lightingApp().run() 
