# =============================================================================
# This code builds a Kivy GUI that can switch two LEDs on/off, using 
# firebase and RaspberryPi. The overall process is as such: User input on 
# laptop using Kivy GUI, user input is sent to be stored in firebase, stored 
# data is pulled from firebase by the RaspberryPi, and RaspberryPi switches the
# LEDs on/off based on the stored data.
# =============================================================================


from kivy.app import App 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.togglebutton import ToggleButton
from firebase import firebase

url = "https://dw-1d-week-4-3af73.firebaseio.com/" # URL to Firebase database
token = "Lqv3YbIogV3o3Q7sAEnotO3Ld0WKzUtjOp1jiSoJ" # unique token used for authentication
firebase=firebase.FirebaseApplication(url,token)

class root_widget(GridLayout):

    rows = 2
    cols = 2
    
    def __init__(self,**kwargs): 
        super(root_widget,self).__init__(**kwargs)
        
# =============================================================================
#       Here, we instantiate our labels and toggle buttons. With respect to 
#       the grid:
#          row 1 col 1 refers to label 1
#          row 1 col 2 refers to toggle button 1
#          row 2 col 1 refers to label 2
#          row 2 col 2 refers to toggle button 2
# =============================================================================
        
        self.l1 = Label(text = "Yellow LED",
                   font_size = 15)
        self.t1 = ToggleButton(text = "off" if firebase.get("/yellow_led_status") == "normal" else "on", # <-- Toggle button makes reference to firebase before displaying text
                          state = firebase.get("/yellow_led_status"),                                    # <-- Toggle button makes reference to firebase before displaying state
                          on_press = self.print_on_1,                                                    # <-- When toggle button is pressed (mouse click), it goes into "down" state; calls on print_on_1 function
                          on_release = self.print_off_1)                                                 # <-- When toggle button is released (let go of mouse click)), it goes into "normal" state; calls on print_off_1 function
        self.l2 = Label(text = "Red LED",
                   font_size = 15)
        self.t2 = ToggleButton(text = "off" if firebase.get("/red_led_status") == "normal" else "on",    # This part is the same as above, but for the red LED
                          state = firebase.get("/red_led_status"),                                       # 
                          on_press = self.print_on_2,                                                    # 
                          on_release = self.print_off_2)                                                 #
        
# =============================================================================
#       The following four lines is where we add the two label widgets and two 
#       toggle button widgets to the root widget.
#       This is necessary because the build/run function in kivy can only 
#       return one object, which is the root widget by convention.
# =============================================================================
        self.add_widget(self.l1)
        self.add_widget(self.t1)
        self.add_widget(self.l2)
        self.add_widget(self.t2)
        
# =============================================================================
#       The following chunk contains the function definitions for the on_press 
#       and on_release events called on earlier.      
# =============================================================================
    def print_on_1(self, event):
        # This changes the text of toggle button 1 to "on"
        self.t1.text = "on"   
        # This stores "down" in the firebase directory for yellow_led_status
        firebase.put("/", "yellow_led_status", "down")
    
    
    def print_on_2(self, event): # Same as above, but for red LED.
        self.t2.text = "on"
        firebase.put("/", "red_led_status", "down")
    
    def print_off_1(self, event): 
        # This function is called when you let go of your mouse click, it will
        # check and set the state and text of toggle button 1.
        if self.t1.state == "down":
            pass
        else:
            self.t1.text = "off"
            firebase.put("/", "yellow_led_status", "normal")
    
    def print_off_2(self, event): # Same as above, but for red LED.
        if self.t2.state == "down":
            pass
        else:
            self.t2.text = "off"
            firebase.put("/", "red_led_status", "normal")
            
class LedcontrollerApp(App): # <-- this class builds the App using the information from root_widget() class
    def build(self):
        return root_widget()
    
if __name__ == "__main__":
    LedcontrollerApp().run()
