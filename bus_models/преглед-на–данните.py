#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 19:17:41 2023

@author: dnt2
"""

import pandas as pd
# from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def parse_datetime(timestamp):
    '''
    Превръща базираната на 1900-01-01 timestamp ISO форматирана дата

    Параметри
    ----------
    timestamp : str
        pandas.read_csv() подава всяка клетка с timestamp преобразувана на str

    Резултат
    -------
    datetime.datetime
        ISO форматирани дата и време до милисекунди
    '''
    return (datetime(1900,1,1) + timedelta(float(timestamp)-2)).isoformat()
    

if __name__ == "__main__":

    # # weather_data = pd.read_csv(weather_csv)

    datetime_columns = ['sched_1_355', 'sched_2_1035', 'sched_3_418', 'sched_4_2543',\
                    'stop_1_355',  'stop_2_1035',  'stop_3_418',  'stop_4_2543']

    bus_data = pd.read_csv('https://raw.githubusercontent.com/mic00s/Summer-School-2023/main/raw%20data/raw_data.csv',\
                               date_parser=parse_datetime, parse_dates=datetime_columns)
    
    
        
    # for col in datetime_columns:
    #     bus_data[col] = pd.to_datetime(bus_data[col], format="%Y-%m-%d-%H-%M")
    
    delta_columns = ['delta_stop1_to_stop2', 'delta_stop2_to_stop3', 'delta_stop3_to_stop4']
    
    # Изваждаме реалните времена на спирките една от друга за да получим пропътуваното време между тях
    bus_data[delta_columns] = \
        (bus_data[['stop_1_355',  'stop_2_1035',  'stop_3_418',  'stop_4_2543']].diff(axis=1)).iloc[:,1:]

    # Превръщаме делтите в секунди    
    for col in delta_columns:
        bus_data[col] = bus_data[col].dt.total_seconds()
            
    
    fig, ax = plt.subplots()
    ax.plot(bus_data.sched_1_355, bus_data.delta_stop1_to_stop2, 'r')
    ax.set_title('stop_1_355 до stop_2_1035')
    ax.set_xlabel('sched_1_355')
    ax.set_ylabel('Време в движение (секунди)')
    ax.grid()

    fig, ax = plt.subplots()
    ax.plot(bus_data.sched_2_1035, bus_data.delta_stop2_to_stop3, 'g')
    ax.set_title('stop_2_1035 до stop_3_418')
    ax.set_xlabel('sched_2_1035')
    ax.set_ylabel('Време в движение (секунди)')
    ax.grid()

    fig, ax = plt.subplots()
    ax.plot(bus_data.sched_3_418, bus_data.delta_stop3_to_stop4, 'b')
    ax.set_title('stop_3_418 до stop_4_2543')
    ax.set_xlabel('sched_3_418')
    ax.set_ylabel('Време в движение (секунди)')
    ax.grid()

