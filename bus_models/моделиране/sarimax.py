#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:14:27 2023

Базирано на:
    https://analyticsindiamag.com/complete-guide-to-sarimax-in-python-for-time-series-modeling/

@author: dnt2
"""


import pandas as pd


# Декомпозиция на тренд и сезонност
from statsmodels.tsa.seasonal import seasonal_decompose 

# Тест за стационарност
from statsmodels.tsa.stattools import adfuller



from statsmodels.tsa.statespace.sarimax import SARIMAX


import matplotlib.pyplot as plt

weather_csv = '/home/dnt2/Spielplatz/Семково–2023/case-public-transport-prediction/weather_data.csv'
data_csv = '/home/dnt2/Spielplatz/Семково–2023/extended_data/bus_data_w_iso_dates_and_delta_times.csv'

datetime_columns = ['sched_1_355', 'sched_2_1035', 'sched_3_418', 'sched_4_2543',\
                'stop_1_355',  'stop_2_1035',  'stop_3_418',  'stop_4_2543']

    
bus_data = pd.read_csv(data_csv, parse_dates=datetime_columns)
weather_data = pd.read_csv(weather_csv, sep=';')
weather_data.fillna(0, inplace=True)
weather_data_short = weather_data[['humidity','rain_1h', 'clouds_all']]

ntrain = int(2*len(bus_data)/3)
 
bus_train = bus_data.iloc[:ntrain,:]
bus_test = bus_data.iloc[ntrain:,:]
weather_train = weather_data_short.iloc[:ntrain,:]
weather_test = weather_data_short.iloc[ntrain:,:]

fig, ax = plt.subplots()
ax.grid('on')
ax.plot(bus_data.sched_1_355, bus_data.t_stop1_to_stop2, c='r')
ax.axhline(bus_data.t_stop1_to_stop2.mean(), c='k', ls='--', lw=1)


model = SARIMAX(bus_train.t_stop1_to_stop2, exog=weather_train, order=(1, 1, 1), seasonal_order=(0,0,0,0))
results = model.fit()
print(results.summary())
forecast = results.get_forecast(steps=len(bus_test), exog=weather_test)
predicted_values = forecast.predicted_mean
ax.plot(bus_data.sched_1_355[ntrain:], predicted_values)
