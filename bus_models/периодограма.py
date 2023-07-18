#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:01:10 2023

Източник: https://stackoverflow.com/questions/34428886/discrete-fourier-transformation-from-a-list-of-x-y-points/34432195#34432195

@author: dnt2
"""

import pandas as pd
import numpy as np
from scipy.signal import lombscargle
import matplotlib.pyplot as plt


data_csv = '/home/dnt2/Spielplatz/Семково–2023/extended_data/bus_data_w_iso_dates_and_delta_times.csv'

datetime_columns = ['sched_1_355', 'sched_2_1035', 'sched_3_418', 'sched_4_2543',\
                'stop_1_355',  'stop_2_1035',  'stop_3_418',  'stop_4_2543']
    
data = pd.read_csv(data_csv, parse_dates=datetime_columns)


np.random.seed(12345)

n = 100
x = np.sort(10*np.random.rand(n))

# # Dominant periodic signal
# y = np.sin(2.5*x)  

# # Add some smaller periodic components
# y += 0.15*np.cos(0.75*x) + 0.2*np.sin(4*x+.1)

# # Add some noise
# y += 0.2*np.random.randn(x.size)

# plt.figure(1)
# plt.plot(x, y, 'b')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid()

# Минимален sampling интервал
dxmin = np.diff(x).min()
duration = x.ptp() # Peak-to-Peak value -- понеже х е монотонно нарастваща ни дава продължителността на данните



freqs = np.linspace(1/duration, n/duration, 5*n)
periodogram = lombscargle(x, y, freqs)

kmax = periodogram.argmax()
print("%8.3f" % (freqs[kmax],))

plt.figure(2)
plt.plot(freqs, np.sqrt(4*periodogram/(5*n)))
plt.xlabel('Frequency (rad/s)')
plt.grid()
plt.axvline(freqs[kmax], color='r', alpha=0.25)
