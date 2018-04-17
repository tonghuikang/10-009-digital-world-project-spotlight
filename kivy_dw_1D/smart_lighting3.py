#10.009 The Digital World 1D Project
#17F04 Group 2

''' KIVY APP SCRIPT '''
'''
This script takes in the duty_list from the 
subscriber script, and runs the Kivy App.
The Kivy App displays usage statistics, and 
allows user input to manually adjust lighting levels.
The input is then published to adjust the 
actual LED lighting levels.
'''
#=============================================================================

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

url = "https://dw2018-1d-project.firebaseio.com/"
secret = "mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL"
fire = firebase.FirebaseApplication(url, secret)

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

Builder.load_string("""
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
<screener>
    transition: FadeTransition()
    Screen: 
        name: "welcome"
        Button:
            text: "welcome"
            on_press: root.current = "main"
            on_press: root.set_adj_val()
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
                        color: [1,1,1,1]
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
                    id: rt_globstat1_l00
                    text: ""
                Label:
                    id: rt_globstat2_l00
                    text: ""
                Button:
                    text: "Quit"
                    on_press: root.on_stop()
                    
                    
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
                    id: s0
                    on_value: root.s0_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l0
                    text: ""
                Label:
                    id: rt_globstat1_l0
                    text: ""
                Label:
                    id: rt_globstat2_l0
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
                    id: s1
                    on_value: root.s1_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l1
                    text: ""
                Label:
                    id: rt_globstat1_l1
                    text: ""
                Label:
                    id: rt_globstat2_l1
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
                    id: s2
                    on_value: root.s2_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l2
                    text: ""
                Label:
                    id: rt_globstat1_l2
                    text: ""
                Label:
                    id: rt_globstat2_l2
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
                    id: s3
                    on_value: root.s3_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l3
                    text: ""
                Label:
                    id: rt_globstat1_l3
                    text: ""
                Label:
                    id: rt_globstat2_l3
                    text: ""
                    
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
                    id: s4
                    on_value: root.s4_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l4
                    text: ""
                Label:
                    id: rt_globstat1_l4
                    text: ""
                Label:
                    id: rt_globstat2_l4
                    text: ""
                    
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
                    id: s5
                    on_value: root.s5_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l5
                    text: ""
                Label:
                    id: rt_globstat1_l5
                    text: ""
                Label:
                    id: rt_globstat2_l5
                    text: ""
                    
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
                    id: s6
                    on_value: root.s6_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l6
                    text: ""
                Label:
                    id: rt_globstat1_l6
                    text: ""
                Label:
                    id: rt_globstat2_l6
                    text: ""
                    
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
                    id: s7
                    on_value: root.s7_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l7
                    text: ""
                Label:
                    id: rt_globstat1_l7
                    text: ""
                Label:
                    id: rt_globstat2_l7
                    text: ""
                    
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
                    id: s8
                    on_value: root.s8_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l8
                    text: ""
                Label:
                    id: rt_globstat1_l8
                    text: ""
                Label:
                    id: rt_globstat2_l8
                    text: ""
                    
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
                    id: s9
                    on_value: root.s9_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l9
                    text: ""
                Label:
                    id: rt_globstat1_l9
                    text: ""
                Label:
                    id: rt_globstat2_l9
                    text: ""
                
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
                    id: s10
                    on_value: root.s10_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l10
                    text: ""
                Label:
                    id: rt_globstat1_l10
                    text: ""
                Label:
                    id: rt_globstat2_l10
                    text: ""
                    
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
                    id: s11
                    on_value: root.s11_func(*args)
                    orientation: "horizontal"
                    min: 0.
                    max: 1.
                Label:
                    id: rt_localstat1_l11
                    text: ""
                Label:
                    id: rt_globstat1_l11
                    text: ""
                Label:
                    id: rt_globstat2_l11
                    text: ""
                Button:
                    text: "save settings"
                    on_release: root.send_adj_list()
                    on_release: root.current= "main"
""")

class screener(ScreenManager):
    
    adj_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
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
        
    def s4_func(self, *args):
        value = args[1]
        self.adj_list[4] = value
        
    def s5_func(self, *args):
        value = args[1]
        self.adj_list[5] = value
        
    def s6_func(self, *args):
        value = args[1]
        self.adj_list[6] = value
        
    def s7_func(self, *args):
        value = args[1]
        self.adj_list[7] = value
        
    def s8_func(self, *args):
        value = args[1]
        self.adj_list[8] = value
        
    def s9_func(self, *args):
        value = args[1]
        self.adj_list[9] = value
        
    def s10_func(self, *args):
        value = args[1]
        self.adj_list[10] = value
    
    def s11_func(self, *args):
        value = args[1]
        self.adj_list[11] = value
        
    def set_adj_val(self):
        init_adj_list = fire.get("/adj_list")
        print(init_adj_list)
        #init_adj_list = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
        self.ids.s0.value  = init_adj_list[0]
        self.ids.s1.value  = init_adj_list[1]
        self.ids.s2.value  = init_adj_list[2]
        self.ids.s3.value  = init_adj_list[3]
        self.ids.s4.value  = init_adj_list[4]
        self.ids.s5.value  = init_adj_list[5]
        self.ids.s6.value  = init_adj_list[6]
        self.ids.s7.value  = init_adj_list[7]
        self.ids.s8.value  = init_adj_list[8]
        self.ids.s9.value  = init_adj_list[9]
        self.ids.s10.value = init_adj_list[10]
        self.ids.s11.value = init_adj_list[11]
        
    def start_stop(self):
        Clock.schedule_interval(self.my_callback, 1)
        
    def on_stop(self):
        App.get_running_app().stop()
            
    def my_callback(self, dt):
    
        txt_f = open("/home/pi/thymio/kivy_dw_1D/duty_list.txt", "r")
        line = txt_f.readline()
        txt_f.close()
        duty_val_raw = line.split(",")

        # normalize 0 - 1 to 0.1 - 1
        duty_val = []
        for val in duty_val_raw:
            new_val = float(val)*0.9 + 0.1
            duty_val.append(new_val)
        float_total = ( ( sum(float(x) for x in duty_val_raw) / 12 ) * 100 )
        
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
        
        self.ids.rt_localstat1_l0.text   = "{}%".format(float(duty_val[0]) * 100)
        self.ids.rt_localstat1_l1.text   = "{}%".format(float(duty_val[1]) * 100)
        self.ids.rt_localstat1_l2.text   = "{}%".format(float(duty_val[2]) * 100)
        self.ids.rt_localstat1_l3.text   = "{}%".format(float(duty_val[3]) * 100)
        self.ids.rt_localstat1_l4.text   = "{}%".format(float(duty_val[4]) * 100)
        self.ids.rt_localstat1_l5.text   = "{}%".format(float(duty_val[5]) * 100)
        self.ids.rt_localstat1_l6.text   = "{}%".format(float(duty_val[6]) * 100)
        self.ids.rt_localstat1_l7.text   = "{}%".format(float(duty_val[7]) * 100)
        self.ids.rt_localstat1_l8.text   = "{}%".format(float(duty_val[8]) * 100)
        self.ids.rt_localstat1_l9.text   = "{}%".format(float(duty_val[9]) * 100)
        self.ids.rt_localstat1_l10.text  = "{}%".format(float(duty_val[10]) * 100)
        self.ids.rt_localstat1_l11.text  = "{}%".format(float(duty_val[11]) * 100)
        """
        self.ids.rt_globalstat1_l00.text = "{}%".format(float_total)
        self.ids.rt_globalstat1_l0.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l1.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l2.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l3.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l4.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l5.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l6.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l7.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l8.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l9.text  = "{}%".format(float_total)
        self.ids.rt_globalstat1_l10.text = "{}%".format(float_total)
        self.ids.rt_globalstat1_l11.text = "{}%".format(float_total)
        self.ids.rt_globalstat2_l00.text = "{}".format(float_total)
        self.ids.rt_globalstat2_l0.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l1.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l2.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l3.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l4.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l5.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l6.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l7.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l8.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l9.text  = "{}".format(float_total)
        self.ids.rt_globalstat2_l10.text = "{}".format(float_total)
        self.ids.rt_globalstat2_l11.text = "{}".format(float_total)
        """
        
    # Publishing
    def send_adj_list(self):
        self.dw1d.publish("adj_list", str(self.adj_list).strip('[]'))
        
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
             print("Connected to broker")
             global Connected
             Connected = True
        else:
             print("Connection failed")
    
    #setting up connection to Google Cloud
    Connected = False
    broker_address="35.197.131.13"
    port = 8883
    print("Creating new instance")
    dw1d = mqtt.Client("DW1Dadjpub")
    dw1d.username_pw_set("sammy","password")  #set usernames and passwords
    dw1d.on_connect = on_connect
    print("Connecting to broker")
    dw1d.connect(broker_address, port=port)   #connect to broker
            
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
