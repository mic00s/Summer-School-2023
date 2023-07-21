#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:14:27 2023

Базирано на:
    https://analyticsindiamag.com/complete-guide-to-sarimax-in-python-for-time-series-modeling/

@author: dnt2
"""


import pandas as pd
import numpy as np
from datetime import timedelta


# Декомпозиция на тренд и сезонност
from statsmodels.tsa.seasonal import seasonal_decompose 

# Тест за стационарност
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error


import matplotlib.pyplot as plt

weather_csv = '/home/dnt2/Spielplatz/Семково–2023/case-public-transport-prediction/weather_data.csv'
data_csv = '/home/dnt2/Spielplatz/Семково–2023/extended_data/bus_data_w_iso_dates_and_delta_times.csv'

datetime_columns = ['sched_1_355', 'sched_2_1035', 'sched_3_418', 'sched_4_2543',\
                'stop_1_355',  'stop_2_1035',  'stop_3_418',  'stop_4_2543']

    
bus_data = pd.read_csv(data_csv, parse_dates=datetime_columns)
bus_data.index = pd.DatetimeIndex(bus_data.sched_1_355)

weather_data = pd.read_csv(weather_csv, sep=';')
weather_data.fillna(0, inplace=True)
weather_data.index = pd.DatetimeIndex(bus_data.sched_1_355)

exog_cols = ['humidity','rain_1h', 'clouds_all']
weather_data_short = weather_data[['humidity', 'rain_1h', 'clouds_all']]

start_of_the_last_two_weeks = bus_data.sched_1_355[-1] - timedelta(weeks=2)

test_data_cutoff = bus_data.index >= start_of_the_last_two_weeks

bus_train = bus_data.loc[~test_data_cutoff,:]
bus_test = bus_data.loc[test_data_cutoff,:]
ntrain = len(bus_train)

weather_train = weather_data_short.iloc[~test_data_cutoff,:]
weather_test = weather_data_short.iloc[test_data_cutoff,:]

# --- SARIMAX на пропътувани времена между спирки ----

delta = 't_stop1_to_stop2_original'
order = (3, 1, 2)
seasonal_order = (1,1,1,4)
c1 = 'r'
c2 = 'c'

model = SARIMAX(bus_train[delta], exog=weather_train, order=order, seasonal_order=seasonal_order)
results = model.fit()
print()
print(results.summary())
forecast = results.get_forecast(steps=len(bus_test), exog=weather_test)

rmse = np.sqrt(mean_squared_error(bus_test[delta], forecast.predicted_mean))
mae  = mean_absolute_error(bus_test[delta], forecast.predicted_mean)
mape = mean_absolute_percentage_error(bus_test[delta], forecast.predicted_mean)

print('\nTecm върху последните две седмици:\nRMSE = {:.2f}   MAE = {:.2f}   MAPE = {:.2f}\n'.format(rmse, mae, mape))

fig, ax = plt.subplots()
ax.grid('on')
ax.plot(bus_data.sched_1_355, bus_data[delta], c=c1)
ax.axhline(bus_data[delta].mean(), c='k', ls='--', lw=1)
ax.plot(bus_data.sched_1_355[ntrain:], forecast.predicted_mean, c=c2)
ax.set_title('{} SARIMAX: {}, {}, exog={}\nRMSE = {:.2f}  MAE = {:.2f}  MAPE = {:.2f}'.\
              format(delta, order, seasonal_order, exog_cols, rmse, mae, mape))
ax.set_ylabel('Време за придвижване (секунди)')
ax.set_xlabel('sched_1_355')



# delta = 't_stop1_to_stop2'
# order = (2, 1, 1)
# seasonal_order = (0,1,1,4)
# c1 = 'r'
# c2 = 'c'

# model = SARIMAX(bus_train[delta], exog=weather_train, order=order, seasonal_order=seasonal_order)
# results = model.fit()
# print()
# print(results.summary())
# forecast = results.get_forecast(steps=len(bus_test), exog=weather_test)

# rmse = np.sqrt(mean_squared_error(bus_test[delta], forecast.predicted_mean))
# mae  = mean_absolute_error(bus_test[delta], forecast.predicted_mean)
# mape = mean_absolute_percentage_error(bus_test[delta], forecast.predicted_mean)

# print('\nTecm върху последните две седмици:\nRMSE = {:.2f}   MAE = {:.2f}   MAPE = {:.2f}\n'.format(rmse, mae, mape))

# fig, ax = plt.subplots()
# ax.grid('on')
# ax.plot(bus_data.sched_1_355, bus_data[delta], c=c1)
# ax.axhline(bus_data[delta].mean(), c='k', ls='--', lw=1)
# ax.plot(bus_data.sched_1_355[ntrain:], forecast.predicted_mean, c=c2)
# ax.set_title('{} SARIMAX: {}, {}, exog={}\nRMSE = {:.2f}  MAE = {:.2f}  MAPE = {:.2f}'.\
#               format(delta, order, seasonal_order, exog_cols, rmse, mae, mape))
# ax.set_ylabel('Време за придвижване (секунди)')
# ax.set_xlabel('sched_1_355')



# delta = 't_stop2_to_stop3'
# order = (2, 1, 2)
# seasonal_order = (1,1,1,4)
# c1 = 'green'
# c2 = 'm'

# model = SARIMAX(bus_train[delta], exog=weather_train, order=order, seasonal_order=seasonal_order)
# results = model.fit()
# print()
# print(results.summary())
# forecast = results.get_forecast(steps=len(bus_test), exog=weather_test)

# rmse = np.sqrt(mean_squared_error(bus_test[delta], forecast.predicted_mean))
# mae  = mean_absolute_error(bus_test[delta], forecast.predicted_mean)
# mape = mean_absolute_percentage_error(bus_test[delta], forecast.predicted_mean)

# print('\nTecm върху последните две седмици:\nRMSE = {:.2f}   MAE = {:.2f}   MAPE = {:.2f}\n'.format(rmse, mae, mape))

# fig, ax = plt.subplots()
# ax.grid('on')
# ax.plot(bus_data.sched_1_355, bus_data[delta], c=c1)
# ax.axhline(bus_data[delta].mean(), c='k', ls='--', lw=1)
# ax.plot(bus_data.sched_1_355[ntrain:], forecast.predicted_mean, c=c2)
# ax.set_title('{} SARIMAX: {}, {}, exog={}\nRMSE = {:.2f}  MAE = {:.2f}  MAPE = {:.2f}'.\
#               format(delta, order, seasonal_order, exog_cols, rmse, mae, mape))
# ax.set_ylabel('Време за придвижване (секунди)')
# ax.set_xlabel('sched_1_355')



# delta = 't_stop3_to_stop4'
# order = (2, 1, 2)
# seasonal_order = (1,1,1,4)
# c1 = 'b'
# c2 = 'y'

# model = SARIMAX(bus_train[delta], exog=weather_train, order=order, seasonal_order=seasonal_order)
# results = model.fit()
# print()
# print(results.summary())
# forecast = results.get_forecast(steps=len(bus_test), exog=weather_test)

# rmse = np.sqrt(mean_squared_error(bus_test[delta], forecast.predicted_mean))
# mae  = mean_absolute_error(bus_test[delta], forecast.predicted_mean)
# mape = mean_absolute_percentage_error(bus_test[delta], forecast.predicted_mean)

# print('\nTecm върху последните две седмици:\nRMSE = {:.2f}   MAE = {:.2f}   MAPE = {:.2f}\n'.format(rmse, mae, mape))

# fig, ax = plt.subplots()
# ax.grid('on')
# ax.plot(bus_data.sched_1_355, bus_data[delta], c=c1)
# ax.axhline(bus_data[delta].mean(), c='k', ls='--', lw=1)
# ax.plot(bus_data.sched_1_355[ntrain:], forecast.predicted_mean, c=c2)
# ax.set_title('{} SARIMAX: {}, {}, exog={}\nRMSE = {:.2f}  MAE = {:.2f}  MAPE = {:.2f}'.\
#               format(delta, order, seasonal_order, exog_cols, rmse, mae, mape))
# ax.set_ylabel('Време за придвижване (секунди)')
# ax.set_xlabel('sched_1_355')

