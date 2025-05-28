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

    # Get and print a single frame of data (time series
    # of voltage per channel)
    data = Osc.get_data(wait_complete= True)
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
