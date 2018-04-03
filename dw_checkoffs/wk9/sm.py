from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
from boxworld import thymio_world

class MySMClass(sm.SM):
    start_state = False  # speed, rot, wall
    def get_next_values(self, state, inp):
        wall = state
        # These two lines is to stop the robot
        # by pressing the backward button.
        # This only works when using the real robot.
        # It will not work in simulator.
        if inp.button_backward:
            return 'halt', io.Action(0,0)
        #####################################
        
        #ground = inp.prox_ground.reflected
        #ground = inp.prox_ground.ambiant
        
        ground = inp.prox_ground.delta
        left = ground[0]
        right = ground[1]
        print(left,right,wall)
        
        next_state = wall
        
        if not wall:
            if left > 200 and right > 200:
                return next_state, io.Action(fv=0.1, rv=0)
            else:
                wall = True
                next_state = wall
                return next_state, io.Action(fv=0.03, rv=1)
        
        print("wall")
        if wall == True:
            print("wall")
            if left > 200 and right > 200: # both white
                print("rv=1")
                return next_state, io.Action(fv=0.03, rv=0.5)
            if left < 200 and right < 200: # both black
                return next_state, io.Action(fv=0.03, rv=-0.5)
            else:
                return next_state, io.Action(fv=0.09, rv=0)

        return next_state, io.Action(fv=0.1, rv=0)
    
    #########################################
    # Don't modify the code below.
    # this is to stop the state machine using
    # inputs from the robot
    #########################################
    def done(self,state):
        if state=='halt':
            return True
        else:
            return False

MySM=MySMClass()

############################

m=ThymioSMReal(MySM)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()


