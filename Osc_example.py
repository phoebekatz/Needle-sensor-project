# This is a example of doing once test using osc instrument include generate a impulse signal and get the response data and plot data
from moku.instruments import Oscilloscope
import numpy as np
import pandas as pd
import os
import CNCcontrol as cc
import matplotlib.pyplot as plt
import time
from mokulib import osc_test_np

# Connect to the Moku device
Osc = Oscilloscope('[fe80::7269:79ff:feb9:332%7]', force_connect=True)
try:
    Osc.set_trigger(type='Edge',source='Output1',level=0)
    # Set the span to from -1ms to 1ms i.e. trigger point centred
    Osc.set_timebase(0, 200e-6,max_length=4096)

    Osc.generate_waveform(1, 'Pulse',pulse_width=1e-6,edge_time=0.5e-6, amplitude=10, frequency=300)
    Osc.set_source(1,'Input1')

    # this is only for geting the time vector you can basicly ingnor this if you dont need to plot value versus time
    data = Osc.get_data(wait_complete= True)
    
    # this is calling the function from mokulib file wrote by myself
    #'ch1' mean the data recived from the first chanel(we only need first chael of the moku both for the input and output) 
    # 20 means taking 20 times test and calculating average of them as the result
    # and it will automaticly return a numpy array
    avertest = osc_test_np(Osc,'ch1',20) 
    print(data['time'][-1])
    print(len(data['time']))
    plt.plot(data['time'],avertest)
    plt.show()


except Exception as e:
    print(f'Exception occurred: {e}')
finally:
    # Close the connection to the Moku device
    # This ensures network resources are released correctly
    Osc.relinquish_ownership()
