from moku.instruments import Oscilloscope
import numpy as np
import pandas as pd
import os
import CNCcontrol as cc
import time
from mokulib import osc_test
safty_height = -1
feedrate = 2000
initial_gcode = [
    'G21 ; millimeters',
    'G90 ; absolute coordinate',
    'G17 ; XY plane',
    'G94 ; units per minute feed rate mode',
    'M3 S1000 ; Turning on spindle',
    # Go to zero location
    f'G0 X0 Y0 Z{safty_height}'
]
go_initial_point = [
    'G90',
    f'G1 Z0 F{feedrate}',
    'G1 X0 Y0'
]
go_test_point1 = [
    'G90',
    f'G1 Z{safty_height} F{feedrate}',
    'G1 X30 Y40',
    'G1 Z-38'
]
go_test_point2 = [
    'G90',
    f'G1 Z{safty_height} F{feedrate}',
    'G1 X60 Y5',
    'G1 Z-38'
]
go_test_point3 = [
    'G90',
    f'G1 Z{safty_height} F{feedrate}',
    'G1 X90 Y40',
    'G1 Z-38'
]
godown_1mm = [
    'G91',
    f'G1 Z-1 F{feedrate}'
]
godown_2mm = [
    'G91',
    f'G1 Z-2 F{feedrate}'
]
turnoff = [
    'M5'
]
go_destination = [
    go_test_point1,
    go_test_point2,
    go_test_point3
]
k = 0
while os.path.exists(f'C:/Xiong/Oil_mix{k}'):
    k += 1
os.makedirs(f'C:/Xiong/Oil_mix{k}', exist_ok=True)
Osc = Oscilloscope('[fe80::7269:79ff:feb9:332%7]', force_connect=True)
cnc = cc.connect_cnc("COM5")
destination = ['oil','water','vinegar']
av_num = 1
try:
    Osc.set_trigger(type='Edge',source='Output1',level=0)
    # Set the span to from -1ms to 1ms i.e. trigger point centred``
    Osc.set_timebase(0, 250e-6,max_length=4096)

    Osc.generate_waveform(1, 'Pulse',pulse_width=0.7e-6,edge_time=0.7e-6, amplitude=10, frequency=2e3)
    Osc.set_source(1,'Input1')
    cc.operate_until_end(initial_gcode,cnc)
    # Get and print a single frame of data (time series
    # of voltage per channel)
    cc.operate_until_end(go_initial_point,cnc)
    time_vector = osc_test(Osc,'time')
    df = pd.DataFrame(time_vector)
    df.to_csv(f'C:/Xiong/Oil_mix{k}/time_vector.csv',index=True)
    loop_count = 10000
    for i in range(loop_count):
        print(f"loop = {i}")
        for q,destination_index in enumerate(destination):
            cc.operate_until_end(go_destination[q],cnc)
            response = osc_test(Osc,'ch1',av_num)
            df = pd.DataFrame(response)
            df.to_csv(f'C:/Xiong/Oil_mix{k}/{destination_index}{i},2mm.csv',index=False)
            for z in range(2):
                cc.operate_until_end(godown_1mm,cnc)
                response = osc_test(Osc,'ch1',av_num)
                df = pd.DataFrame(response)
                df.to_csv(f'C:/Xiong/Oil_mix{k}/{destination_index}{i},{2+z+1}mm.csv',index=False)
except Exception as e:
    print(f'Exception occurred: {e}')
finally:
    # Close the connection to the Moku device
    # This ensures network resources are released correctly
    Osc.relinquish_ownership()
    cc.operate_until_end(go_initial_point,cnc)
    cc.operate_until_end(turnoff,cnc)