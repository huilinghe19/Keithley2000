import os
import time
from sardana import State
from sardana.pool.controller import CounterTimerController, Type,\
    Description, DefaultValue
import random
from epics import *
def read_keithley():
    return caget('iockeithley1:voltage')
    #return int(random.randint(1000,2000))


class KeithleyCounterTimerController(CounterTimerController):
    """This controller provides interface for network packages counting.
    It counts the number of bytes of data transmitted or received by a network
    interface over the integration time.
    """


    def __init__(self, inst, props, *args, **kwargs):
        CounterTimerController.__init__(self,inst,props, *args, **kwargs)
        self.acq_time = 1.
        self.acq_end_time = time.time()
        self.start_counts = 0

    def LoadOne(self, axis, value):
        self.acq_time = value

    def StateOne(self, axis):
        state = State.On
        if time.time() < self.acq_end_time:
            state = State.Moving
        # due to sardana-org/sardana #621 we need to return also status
        status_string = 'My custom status info'
        return state, status_string

    def StartOne(self, axis, _):
        self.acq_end_time = time.time() + self.acq_time
        # self.start_counts = read_keithley()
        caput('iockeithley1:voltage.PROC', 1)

    # due to sardana-org/sardana #622 we need to implement StartAll
    def StartAll(self):
        pass

    def ReadOne(self, axis):
        counts = read_keithley()
	return counts
        #return counts -  self.start_counts

    def AbortOne(self, axis):
        self.acq_end_time = time.time()
