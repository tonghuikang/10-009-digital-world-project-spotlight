from kivy.app import App 

from kivy.uix.gridlayout import GridLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from firebase import firebase

import paho.mqtt.client as mqtt

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

url = "https://dw2018-1d-project.firebaseio.com/"
secret = 'mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL'
fire = firebase.FirebaseApplication(url, secret)

Builder.load_string("""
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
<screener>
    transition: FadeTransition()
    Screen: 
        name: "welcome"
        Button:
            text: "welcome"
            on_press: root.current = "main"
            on_press: root.start_stop()
    Screen:
        name: "main"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    ImageButton:
                        id: b0
                        source: "led-light.png"
                        color: []
                        on_press: root.current = "adj_0"
                    ImageButton:
                        id: b4
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_4"
                    ImageButton:
                        id: b8
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_8"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    ImageButton:
                        id: b1
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_1"
                    ImageButton:
                        id: b5
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_5"
                    ImageButton:
                        id: b9
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_9"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    ImageButton:
                        id: b2
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_2"
                    ImageButton:
                        id: b6
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_6"
                    ImageButton:
                        id: b10
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_10"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    ImageButton:
                        id: b3
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_3"
                    ImageButton:
                        id: b7
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_7"
                    ImageButton:
                        id: b11
                        source: "led-light.png"
                        color: [1,1,1,1]
                        on_press: root.current = "adj_11"
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Label:
                    id: blank_stat
                Label:
                    id: blank_stat_2
                Label:
                    id: stat_3
                    text: "Usage"
                Label:
                    id: stat_4
                    text: "Usage"
                Label: 
                    
                    
    Screen:
        name: "adj_0"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Image:
                        id: i0
                        source: "led-light.png"
                        color: [1,1,1,1]                      
                    Label:
                    Label:

                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i0_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_stat_i0
                    text: "Usage" # root.get_rt_stat_i0()
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
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
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Image:
                        id: i1
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i1_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
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
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Image:
                        id: i2
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i2_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
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
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Image:
                        id: i3
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i3_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_4"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:                       
                    Image:
                        id: i4
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i4_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_5"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label
                    Image:
                        id: i5
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i5_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_6"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Image:
                        id: i6
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i6_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_7"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Image:
                        id: i7
                        source: "led-light.png"
                        color: [1,1,1,1]
                    Label:
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i7_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_8"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Image:
                        id: i8
                        source: "led-light.png"
                        color: [1,1,1,1]
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i8_ctrl

                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_9"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Image:
                        id: i9
                        source: "led-light.png"
                        color: [1,1,1,1]
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i9_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_10"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Image:
                        id: i10
                        source: "led-light.png"
                        color: [1,1,1,1]
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i10_ctrl

                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                    
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
                    
    Screen:
        name: "adj_11"
        BoxLayout:
            orientation: "horizontal"
            cols: 2
            BoxLayout:
                cols: 4
                orientation: "horizontal"
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Label:
                BoxLayout:
                    rows: 3
                    orientation: "vertical"
                    Label:
                    Label:
                    Image:
                        id: i11
                        source: "led-light.png"
                        color: [1,1,1,1]
        
            BoxLayout:
                rows: 5
                orientation: "vertical"
                Slider:
                    value: root.i11_ctrl
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: stat_2
                    text: "Usage"
                Label:
                    id: stat_3
                    text: "Usage"
                Label: 
                    id: stat_4
                    text: "Usage"
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
""")

class screener(ScreenManager):
    
    def __init__(self):
        self.i0_ctrl = NumericProperty(1.0)
        self.i1_ctrl = NumericProperty(1.0)
        self.i2_ctrl = NumericProperty(1.0)
        self.i3_ctrl = NumericProperty(1.0)
        self.i4_ctrl = NumericProperty(1.0)
        self.i5_ctrl = NumericProperty(1.0)
        self.i6_ctrl = NumericProperty(1.0)
        self.i7_ctrl = NumericProperty(1.0)
        self.i8_ctrl = NumericProperty(1.0)
        self.i9_ctrl = NumericProperty(1.0)
        self.i10_ctrl = NumericProperty(1.0)
        self.i11_ctrl = NumericProperty(1.0)
        
        self.adj_list = [self.i0_ctrl, self.i1_ctrl, self.i2_ctrl, self.i3_ctrl, self.i4_ctrl, self.i5_ctrl, self.i6_ctrl, self.i7_ctrl, self.i8_ctrl, self.i9_ctrl, self.i10_ctrl, self.i11_ctrl]

        #setting up connection to Google Cloud
        self.Connected = False
        self.broker_address="35.197.131.13"
        self.port = 8883
        print("Creating new instance")
        self.dw1d = mqtt.Client("DW1Dbetybhty")
        self.dw1d.username_pw_set("sammy","password")  #set usernames and passwords
        self.dw1d.on_connect = on_connect
        print("Connecting to broker")
        self.dw1d.connect(self.broker_address, port=self.port)   #connect to broker


    def start_stop(self):
        Clock.schedule_interval(self.my_callback, 1)
            
    def my_callback(self, dt):
        try:
            txt_f = open("/home/pi/Desktop/duty_list.txt", "r")
            line = txt_f.readline()
            txt_f.close()
            duty_val = line.split(",")
            self.ids.b0.color   = [1,1,1, (duty_val[0])]
            self.ids.i0.color   = [1,1,1, (duty_val[0])]
            self.ids.b1.color   = [1,1,1, (duty_val[1])]
            self.ids.i1.color   = [1,1,1, (duty_val[1])]
            self.ids.b2.color   = [1,1,1, (duty_val[2])]
            self.ids.i2.color   = [1,1,1, (duty_val[2])]
            self.ids.b3.color   = [1,1,1, (duty_val[3])]
            self.ids.i3.color   = [1,1,1, (duty_val[3])]
            self.ids.b4.color   = [1,1,1, (duty_val[4])]
            self.ids.i4.color   = [1,1,1, (duty_val[4])]
            self.ids.b5.color   = [1,1,1, (duty_val[5])]
            self.ids.i5.color   = [1,1,1, (duty_val[5])]
            self.ids.b6.color   = [1,1,1, (duty_val[6])]
            self.ids.i6.color   = [1,1,1, (duty_val[6])]
            self.ids.b7.color   = [1,1,1, (duty_val[7])]
            self.ids.i7.color   = [1,1,1, (duty_val[7])]
            self.ids.b8.color   = [1,1,1, (duty_val[8])]
            self.ids.i8.color   = [1,1,1, (duty_val[8])]
            self.ids.b9.color   = [1,1,1, (duty_val[9])]
            self.ids.i9.color   = [1,1,1, (duty_val[9])]
            self.ids.b10.color  = [1,1,1, (duty_val[10])]
            self.ids.i10.color  = [1,1,1, (duty_val[10])]
            self.ids.b11.color  = [1,1,1, (duty_val[11])]
            self.ids.i11.color  = [1,1,1, (duty_val[11])]
        except:
            pass

    # Publishing
    def send_adj_list(self):
        self.dw1d.publish("adj_list", str(adj_list))
        
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
             print("Connected to broker")
             global Connected
             Connected = True
        else:
             print("Connection failed")
    


# =============================================================================
#     def get_rt_stat_i0(self):
#         rt_stat = fire.get("/rt_stat_i0")
#         self.ids.rt_stat_i0.text = "Saved: {}%".format(round(rt_stat,2))
# =============================================================================
            
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
    
    def on_press(self):
        pass
            
class smart_lightingApp(App):
    def build(self):
        return screener()

if __name__ == "__main__":
    smart_lightingApp().run() 
