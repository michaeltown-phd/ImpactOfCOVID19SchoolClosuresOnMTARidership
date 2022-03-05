#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:26:51 2021

@author: michaeltown
"""

## beginning of module 1 MVP data analysis

import numpy as np
import pandas as pd
import os as os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

## revised EDA project to look for patterns in MTA ridership due to COVID19 restrictions

## filter functions

# from year to year each SCP jumps a lot
def filterLargeDiff(x):
    if (x < 2500) & (x > 0):
        return x;
    else:
        return np.nan;

def weekdayfilter(x):
    return x.DOW < 5;


# date limits
lowerDate = pd.to_datetime('2020-11-10');
upperDate = pd.to_datetime('2020-11-30');

# mta data load
dataFileLoc = '/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/data/mtaData202002-202110.csv';
mtaData = pd.read_csv(dataFileLoc);

# covid19 data load
dataFileLoc1 = '/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/data/timeLineOfCOVID19_NYC_schools.csv';
covid19Data = pd.read_csv(dataFileLoc1);
covid19Data['Date']= pd.to_datetime(covid19Data.Date);


## COVID19

# convert date time
mtaData['DATETIME'] = pd.to_datetime(mtaData.DATE + ' ' +mtaData.TIME);
mtaData['DATE']= pd.to_datetime(mtaData.DATE);
mtaData['HOUR'] = mtaData.DATETIME.dt.hour
mtaData['NEXT_ENTRIES'] = mtaData.ENTRIES.shift(-1);
mtaData['NEXT_EXITS'] = mtaData.EXITS.shift(-1);
mtaData = mtaData.sort_values(by=['UNIT','SCP']);

mtaData['ENTRIES_4HR'] = mtaData.NEXT_ENTRIES-mtaData.ENTRIES;
mtaData['EXITS_4HR'] = mtaData.NEXT_EXITS-mtaData.EXITS;

mtaData.dropna();

mtaData.ENTRIES_4HR = mtaData.ENTRIES_4HR.apply(filterLargeDiff);
mtaData.EXITS_4HR = mtaData.EXITS_4HR.apply(filterLargeDiff);
mtaData['DOW'] = mtaData.DATETIME.dt.dayofweek;
mtaData['WKDAY'] = mtaData.DOW < 5;
mtaData['WKEND'] = mtaData.DOW > 4;
wkdayid = lambda x : 'WKDAY' if x < 5 else 'WKEND';
mtaData['WKDAYID'] = mtaData.DOW.apply(wkdayid);

    
# find the entries and exits each 4 hour time period, 
    
gMtaDataSumWKDY = mtaData.groupby(['DATE','WKDAYID'])['ENTRIES_4HR','EXITS_4HR'].sum();
gMtaDataSumWKND = mtaData.groupby(['DATE','WKDAYID'])['ENTRIES_4HR','EXITS_4HR'].sum();


# flatten these data
gMtaDataSumWKDY = gMtaDataSumWKDY.unstack(level= 1);     

fig1 = plt.figure();
ax1 = fig1.add_subplot(111);
for i in range(len(covid19Data.EventShort)):
    ax1.text(covid19Data.Date.iloc[i],3000000,covid19Data.EventShort.iloc[i],rotation=90,fontsize = 7);

plt.plot(gMtaDataSumWKDY.index,gMtaDataSumWKDY.ENTRIES_4HR.WKDAY,'-',color = 'blue');
plt.plot(gMtaDataSumWKDY.index,gMtaDataSumWKDY.EXITS_4HR.WKDAY,'-.',color='black');
plt.plot(gMtaDataSumWKDY.index,gMtaDataSumWKDY.ENTRIES_4HR.WKEND,'-',color = 'lightblue');
plt.plot(gMtaDataSumWKDY.index,gMtaDataSumWKDY.EXITS_4HR.WKEND,'-.',color='gray');


plt.title('MTA Entries/Exits for all MTA Stations during COVID19 Era');
plt.xlabel('hour of day');
plt.ylabel('Entries/exits per day');
plt.grid();
plt.ylim([-1000,6000000])
plt.legend(['entries-wkdy','exits-wkdy','entries-wknd','exits-wknd'],loc = 'upper right');
plt.show;
os.chdir('/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/figures')
fig1.savefig('allMTAstations-timeSeries_202002-202110.jpg')
 

fig4 = plt.figure();
ax4 = fig4.add_subplot(111);
# remove this so that the plot doesn't extend past the focus time period
# for i in range(len(covid19Data.EventShort)):
#     ax2.text(covid19Data.Date.iloc[i],40000,covid19Data.EventShort.iloc[i],rotation=90,fontsize = 8);

limInd = (gMtaDataSumWKDY.index>lowerDate) & (gMtaDataSumWKDY.index<upperDate);
plt.plot(gMtaDataSumWKDY.index[limInd],gMtaDataSumWKDY.ENTRIES_4HR.WKDAY[limInd],'-',color = 'blue');
plt.plot(gMtaDataSumWKDY.index[limInd],gMtaDataSumWKDY.EXITS_4HR.WKDAY[limInd],'-.',color='black');
plt.plot(gMtaDataSumWKDY.index[limInd],gMtaDataSumWKDY.ENTRIES_4HR.WKEND[limInd],'-',color = 'lightblue');
plt.plot(gMtaDataSumWKDY.index[limInd],gMtaDataSumWKDY.EXITS_4HR.WKEND[limInd],'-.',color='gray');

plt.title('MTA Entries/Exits for all stations during COVID19 (focus time pd)'); 
plt.xlabel('hour of day');
plt.xticks(rotation = 90)
plt.ylabel('Entries/exits per day');
plt.grid();
plt.ylim([-1000,6000000])
plt.xlim([lowerDate,upperDate])
plt.legend(['entries-wkdy','exits-wkdy','entries-wknd','exits-wknd'],loc = 'upper right');
plt.show;
os.chdir('/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/figures')
fig4.savefig('allMTAstations-timeSeries_20211110-20211130.jpg')


#hourlyBins = [0,4,8,12,16,20,24];
#hourlyLabels= ['0-4','4-8','8-12','12-16','16-20','20-24'];

# test cases 
#stationNames = ['BROOKLYN BRIDGE', 'CITY HALL'];
#stationNames = ['BROOLYN BRIDGE'];
#for station in stationNames:


for station in mtaData.STATION.unique():  #used this to loop through all data in exploratory analysis
    
    mtaDataLoop = mtaData[(mtaData.STATION == station)].loc[:,['DATE', 'UNIT','SCP','TIME','HOUR','DATETIME','STATION','ENTRIES','EXITS','NEXT_ENTRIES','NEXT_EXITS','ENTRIES_4HR','EXITS_4HR','WKDAYID',]];

    # this aspect of the loop was to economize when not analyzing all data
    # mtaDataLoop['DOW'] = mtaDataLoop.DATETIME.dt.dayofweek;
    # mtaDataLoop['WKDAY'] = mtaDataLoop.DOW < 5;
    # mtaDataLoop['WKEND'] = mtaDataLoop.DOW > 4;
    # wkdayid = lambda x : 'WKDAY' if x < 5 else 'WKEND';
    # mtaDataLoop['WKDAYID'] = mtaDataLoop.DOW.apply(wkdayid);
    
     
    # filter for the year-to-year jumps
    mtaDataLoop.ENTRIES_4HR = mtaDataLoop.ENTRIES_4HR.apply(filterLargeDiff);
    mtaDataLoop.EXITS_4HR = mtaDataLoop.EXITS_4HR.apply(filterLargeDiff);
    
    # find the entries and exits each 4 hour time period, 
    
    gMtaDataLoopSumWKDY = mtaDataLoop.groupby(['DATE','WKDAYID'])['ENTRIES_4HR','EXITS_4HR'].sum();
    gMtaDataLoopSumWKND = mtaDataLoop.groupby(['DATE','WKDAYID'])['ENTRIES_4HR','EXITS_4HR'].sum();

    # flatten these data
    gMtaDataLoopSumWKDY = gMtaDataLoopSumWKDY.unstack(level= 1);     


    # weekday and weekend plots
    fig2 = plt.figure();
    ax2 = fig2.add_subplot(111);
    for i in range(len(covid19Data.EventShort)):
        ax2.text(covid19Data.Date.iloc[i],40000,covid19Data.EventShort.iloc[i],rotation=90,fontsize = 7);

    plt.plot(gMtaDataLoopSumWKDY.index,gMtaDataLoopSumWKDY.ENTRIES_4HR.WKDAY,'-',color = 'blue');
    plt.plot(gMtaDataLoopSumWKDY.index,gMtaDataLoopSumWKDY.EXITS_4HR.WKDAY,'-.',color='black');
    plt.plot(gMtaDataLoopSumWKDY.index,gMtaDataLoopSumWKDY.ENTRIES_4HR.WKEND,'-',color = 'lightblue');
    plt.plot(gMtaDataLoopSumWKDY.index,gMtaDataLoopSumWKDY.EXITS_4HR.WKEND,'-.',color='gray');


    plt.title('MTA Entries/Exits for ' + station + ' during COVID19 Era');
    plt.xlabel('hour of day');
    plt.ylabel('Entries/exits per day');
    plt.grid();
    plt.ylim([-1000,100000])
    plt.legend(['entries-wkdy','exits-wkdy','entries-wknd','exits-wknd'],loc = 'upper right');
    plt.show;
    os.chdir('/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/figures')
    fig2.savefig(station.replace(' ','').replace('/','')+'-timeSeries_202002-202110.jpg')


#   limiting to November closure -- having trouble plotting the limited indexes here
    fig3 = plt.figure();
    ax3 = fig3.add_subplot(111);
    # for i in range(len(covid19Data.EventShort)):
    #     ax2.text(covid19Data.Date.iloc[i],40000,covid19Data.EventShort.iloc[i],rotation=90,fontsize = 8);

    limInd = (gMtaDataLoopSumWKDY.index>lowerDate) & (gMtaDataLoopSumWKDY.index<upperDate);
    plt.plot(gMtaDataLoopSumWKDY.index[limInd],gMtaDataLoopSumWKDY.ENTRIES_4HR.WKDAY[limInd],'-',color = 'blue');
    plt.plot(gMtaDataLoopSumWKDY.index[limInd],gMtaDataLoopSumWKDY.EXITS_4HR.WKDAY[limInd],'-.',color='black');
    plt.plot(gMtaDataLoopSumWKDY.index[limInd],gMtaDataLoopSumWKDY.ENTRIES_4HR.WKEND[limInd],'-',color = 'lightblue');
    plt.plot(gMtaDataLoopSumWKDY.index[limInd],gMtaDataLoopSumWKDY.EXITS_4HR.WKEND[limInd],'-.',color='gray');

    plt.title('MTA Entries/Exits for ' + station + ' during COVID19 (focus time pd)'); 
    plt.xlabel('hour of day');
    plt.xticks(rotation = 90)
    plt.ylabel('Entries/exits per day');
    plt.grid();
    plt.ylim([-1000,100000])
    plt.xlim([lowerDate,upperDate])
    plt.legend(['entries-wkdy','exits-wkdy','entries-wknd','exits-wknd'],loc = 'upper right');
    plt.show;
    os.chdir('/home/michaeltown/work/metis/modules/exploratoryDataAnalysis/figures')
    fig3.savefig(station.replace(' ','').replace('/','')+'-timeSeries_20211110-20211130.jpg')

