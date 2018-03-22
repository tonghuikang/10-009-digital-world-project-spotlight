from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
from boxworld import thymio_world

class MySMClass(sm.SM):
    start_state=0,0
    def get_next_values(self, state, inp):
        fv_, rv_ = state
        # These two lines is to stop the robot
        # by pressing the backward button.
        # This only works when using the real robot.
        # It will not work in simulator.
        if inp.button_backward:
            return 'halt', io.Action(0,0)
        #####################################
        ground = inp.prox_ground.reflected
        #ground = inp.prox_ground.ambiant
        #ground = inp.prox_ground.delta
        left = ground[0]
        right = ground[1]
        print(left,right)
        if left < 200 and right < 200:
            return 'halt', io.Action(0,0)
        else:
            next_state = state
            return next_state, io.Action(fv=0.10, rv=0.10)

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

#m=ThymioSMSim(MySM, thymio_world)
m=ThymioSMReal(MySM)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()
