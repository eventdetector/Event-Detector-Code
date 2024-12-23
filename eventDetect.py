# -*- coding : utf-8 -*-
# coding: utf-8
import numpy as np
import scipy.signal
from numpy import trapz
from utils import mean_index
import os

def eventDownFast(rawSignal, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, fileName, sampleRate, fileNumber):
    padLen = np.int64(sampleRate)
    prepadded = np.ones(padLen) * np.mean(rawSignal[0:1000])
    signalToFilter = np.concatenate((prepadded, rawSignal))
    rawSignal_list = rawSignal
    rawSignal = np.array(rawSignal)

    mlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], signalToFilter)
    vlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], np.square(signalToFilter - mlTemp))

    ml = np.delete(mlTemp, np.arange(padLen))
    vl = np.delete(vlTemp, np.arange(padLen))

    sl = ml - startCoeff * np.sqrt(vl)
    Ni = len(rawSignal)
    points = np.array(np.where(rawSignal <= sl)[0])
    to_pop = np.array([])
    for i in range(1, len(points)):
        if points[i] - points[i - 1] == 1:
            to_pop = np.append(to_pop, i)
    to_pop = np.int64(to_pop)
    points = np.unique(np.delete(points, to_pop))
    NumberOfEvents = 0;
    RoughEventLocations = np.zeros((100000, 3))
    event_current = np.zeros((100000, 15))

    for i in points:
        event_start_mean = ml[i - 100]
        if i >= Ni - 10:
            break
        start = i
        El = ml[i] - endCoeff * np.sqrt(vl[i])
        while rawSignal[i + 1] < El and i <= Ni - 10:
            i = i + 1
        if ((minDuration * sampleRate / 1000) < (i + 1 - start)) and (
                (i + 1 - start) < (maxDuration * sampleRate / 1000)) and (
                event_start_mean - min(rawSignal[start:i + 1])) > 0:
            NumberOfEvents = NumberOfEvents + 1
            RoughEventLocations[NumberOfEvents - 1, 2] = i + 1 - start
            RoughEventLocations[NumberOfEvents - 1, 0] = start
            RoughEventLocations[NumberOfEvents - 1, 1] = i + 1
            print(rawSignal[start:i + 1])
            min_index = np.argmax(rawSignal[start:i + 1]) + start
            mean_index_left = mean_index(rawSignal_list[start:min_index]) + start
            mean_index_right = mean_index(rawSignal_list[min_index:i + 1]) + min_index
            event_current[NumberOfEvents - 1, 0] = (event_start_mean - min(rawSignal[start:i + 1]))
            event_current[NumberOfEvents - 1, 1] = event_start_mean
            event_current[NumberOfEvents - 1, 2] = abs(
                event_current[NumberOfEvents - 1, 0] / event_current[NumberOfEvents - 1, 1]) * 10000
            event_current[NumberOfEvents - 1, 3] = (event_start_mean - max(rawSignal[start:i + 1]))
            event_current[NumberOfEvents - 1, 4] = trapz(rawSignal[start:i + 1], dx=2)
            event_current[NumberOfEvents - 1, 5] = rawSignal[start] - rawSignal[start + 10]
            event_current[NumberOfEvents - 1, 6] = rawSignal[i] - rawSignal[i - 10]
            event_current[NumberOfEvents - 1, 7] = (min_index - start) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 8] = (i + 1 - min_index) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 9] = (min_index - mean_index_left) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 10] = (mean_index_right - min_index) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 11]=start
            event_current[NumberOfEvents - 1, 12]=i+1

    event_statistic = np.zeros((NumberOfEvents, 15))

    event_statistic[:, 0] = event_current[0: NumberOfEvents, 11] 
    event_statistic[:, 1] = event_current[0: NumberOfEvents, 12] 
    event_statistic[:, 2] = RoughEventLocations[0: NumberOfEvents, 2] / sampleRate * 1000  
    event_statistic[:, 3] = event_current[0: NumberOfEvents, 0]    
    event_statistic[:, 4] = event_current[0: NumberOfEvents, 1]    
    event_statistic[:, 5] = event_current[0: NumberOfEvents, 2]   
    event_statistic[:, 6] = event_current[0: NumberOfEvents, 3]    
    event_statistic[:, 7] = event_current[0: NumberOfEvents, 0] - event_current[0: NumberOfEvents, 3] 
    event_statistic[:, 8] = event_current[0: NumberOfEvents, 4]  
    event_statistic[:, 9] = np.abs(event_current[0: NumberOfEvents, 5])  
    event_statistic[:, 10] = np.abs(event_current[0: NumberOfEvents, 6]) 
    event_statistic[:, 11] =event_current[0: NumberOfEvents, 7]  
    event_statistic[:, 12] =event_current[0: NumberOfEvents, 8] 
    event_statistic[:, 13]=event_current[0: NumberOfEvents, 9]  
    event_statistic[:, 14]=event_current[0: NumberOfEvents, 10] 

    with open(fileName, "a+") as fp:
        np.savetxt(fp, event_statistic, fmt='%.3f', delimiter="\t")
    print("Fast Detect Mode")




def eventUpFast(rawSignal, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, fileName, sampleRate,
                fileNumber, iterNumber):
    padLen = np.int64(sampleRate)
    prepadded = np.ones(padLen) * np.mean(rawSignal[0:1000])
    signalToFilter = np.concatenate((prepadded, rawSignal))
    rawSignal_list = rawSignal
    rawSignal = np.array(rawSignal)

    mlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], signalToFilter)
    vlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], np.square(signalToFilter - mlTemp))

    ml = np.delete(mlTemp, np.arange(padLen))
    vl = np.delete(vlTemp, np.arange(padLen))

    sl = ml + startCoeff * np.sqrt(vl)
    Ni = len(rawSignal)
    points = np.array(np.where(rawSignal >= sl)[0])
    to_pop = np.array([])
    for i in range(1, len(points)):
        if points[i] - points[i - 1] == 1:
            to_pop = np.append(to_pop, i)
    to_pop = np.int64(to_pop)
    points = np.unique(np.delete(points, to_pop))
    NumberOfEvents = 0;
    RoughEventLocations = np.zeros((100000, 3))
    event_current = np.zeros((100000, 11))

    for i in points:
        event_start_mean = ml[i - 100]
        if i >= Ni - 10:
            break;
        start = i
        El = ml[i] + endCoeff * np.sqrt(vl[i])
        while rawSignal[i + 1] > El and i <= Ni - 10:
            i = i + 1
        if ((minDuration * sampleRate / 1000) < (i + 1 - start)) and (
                (i + 1 - start) < (maxDuration * sampleRate / 1000)) and (
                max(rawSignal[start:i + 1]) - event_start_mean) > 0:
            NumberOfEvents = NumberOfEvents + 1
            RoughEventLocations[NumberOfEvents - 1, 2] = i + 1 - start
            RoughEventLocations[NumberOfEvents - 1, 0] = start
            RoughEventLocations[NumberOfEvents - 1, 1] = i + 1
            min_index = np.argmax(rawSignal[start:i + 1]) + start
            mean_index_left = mean_index(rawSignal_list[start:min_index]) + start
            mean_index_right = mean_index(rawSignal_list[min_index:i + 1]) + min_index
            event_current[NumberOfEvents - 1, 0] = (event_start_mean - min(rawSignal[start:i + 1]))
            event_current[NumberOfEvents - 1, 1] = event_start_mean
            event_current[NumberOfEvents - 1, 2] = abs(
                event_current[NumberOfEvents - 1, 0] / event_current[NumberOfEvents - 1, 1]) * 10000
            event_current[NumberOfEvents - 1, 3] = (event_start_mean - max(rawSignal[start:i + 1]))
            event_current[NumberOfEvents - 1, 4] = trapz(rawSignal[start:i + 1], dx=2)
            event_current[NumberOfEvents - 1, 5] = rawSignal[start] - rawSignal[start + 10]
            event_current[NumberOfEvents - 1, 6] = rawSignal[i] - rawSignal[i - 10]
            event_current[NumberOfEvents - 1, 7] = (min_index - start) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 8] = (i + 1 - min_index) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 9] = (min_index - mean_index_left) / sampleRate * 1000
            event_current[NumberOfEvents - 1, 10] = (mean_index_right - min_index) / sampleRate * 1000

    event_statistic = np.zeros((NumberOfEvents, 11))
    event_statistic[:, 0] = RoughEventLocations[0: NumberOfEvents, 2] / sampleRate * 1000
    event_statistic[:, 1] = event_current[0: NumberOfEvents, 0]
    event_statistic[:, 2] = event_current[0: NumberOfEvents, 3]
    event_statistic[:, 3] = event_current[0: NumberOfEvents, 0] - event_current[0: NumberOfEvents, 3]
    event_statistic[:, 4] = event_current[0: NumberOfEvents, 4]
    event_statistic[:, 5] = event_current[0: NumberOfEvents, 5]
    event_statistic[:, 6] = event_current[0: NumberOfEvents, 6]
    event_statistic[:, 7] = event_current[0: NumberOfEvents, 7]
    event_statistic[:, 8] = event_current[0: NumberOfEvents, 8]
    event_statistic[:, 9] = event_current[0: NumberOfEvents, 9]
    event_statistic[:, 10] = event_current[0: NumberOfEvents, 10]

    with open(fileName, "a+") as fp:
        np.savetxt(fp, event_statistic, fmt='%.3f', delimiter="\t")
