# -*- coding : utf-8 -*-
# coding: utf-8
import numpy as np
import pyabf
import scipy.signal
from numpy import trapz
from scipy.signal import butter, filtfilt, find_peaks

from utils import mean_index
import os


def eventDownAccurate(rawSignal, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, fileName, sampleRate, fileNumber,windowSize,bufferSize,stepSize):

    window_size = windowSize  # Define the window size

    Ni = len(rawSignal)
    NumberOfEvents = 0
    RoughEventLocations = np.zeros((100000, 3))
    event_current = np.zeros((100000, 15))

    buffer_size = bufferSize  # Define the buffer size
    step_size = stepSize  # Define the step size for overlapping windows

    # Slide the window across the signal
    for w in range(window_size + buffer_size, len(rawSignal), step_size):
        # Check if there is enough data for the buffer
        if w - window_size - buffer_size < 0 or w + buffer_size > len(rawSignal):
            continue
        # Get the data in the window and the buffer
        window_data = rawSignal[w - window_size - buffer_size:w + buffer_size]

        padLen = np.int64(sampleRate)
        prepadded = np.ones(padLen) * np.mean(window_data[0:1000])
        signalToFilter = np.concatenate((prepadded, window_data))
        rawSignal_list = rawSignal

        # Calculate ml and vl for this window
        ml_temp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], signalToFilter)
        vl_temp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], np.square(signalToFilter - ml_temp))

        ml = np.delete(ml_temp, np.arange(padLen))
        vl = np.delete(vl_temp, np.arange(padLen))

        # Calculate the thresholds for this window
        sl = ml - startCoeff * np.sqrt(vl)

        # Event detection
        points = np.array(np.where(window_data[buffer_size:-buffer_size] <= sl[buffer_size:-buffer_size])[0])
        to_pop = np.array([])
        for p in range(1, len(points)):
            if points[p] - points[p - 1] == 1:
                to_pop = np.append(to_pop, p)
        to_pop = np.int64(to_pop)
        points = np.unique(np.delete(points, to_pop))

        # If points is empty, continue to the next window
        if len(points) == 0:
            continue

        for idx in points:
            event_start_mean = ml[idx - 100]
            if idx >= window_size - 10:
                break
            start = idx
            El = ml[idx] - endCoeff * np.sqrt(vl[idx])
            while window_data[idx + 1 + buffer_size] < El and idx <= window_size - 10:
                idx = idx + 1
            if ((minDuration * sampleRate / 1000) < (idx + 1 - start)) and (
                    (idx + 1 - start) < (maxDuration * sampleRate / 1000)) and (
                    event_start_mean - min(window_data[start + buffer_size:idx + 1 + buffer_size])) > 0:
                start = start + w - window_size  # Add shift
                end = idx + 1 + w - window_size
                NumberOfEvents = NumberOfEvents + 1
                RoughEventLocations[NumberOfEvents - 1, 2] = end - start
                RoughEventLocations[NumberOfEvents - 1, 0] = start
                RoughEventLocations[NumberOfEvents - 1, 1] = end
                print(rawSignal[start:end])
                min_index = np.argmax(rawSignal[start:end]) + start
                mean_index_left = mean_index(rawSignal_list[start:min_index]) + start
                mean_index_right = mean_index(rawSignal_list[min_index:end]) + min_index
                event_current[NumberOfEvents - 1, 0] = (event_start_mean - min(rawSignal[start:end]))
                event_current[NumberOfEvents - 1, 1] = event_start_mean
                event_current[NumberOfEvents - 1, 2] = abs(
                    event_current[NumberOfEvents - 1, 0] / event_current[NumberOfEvents - 1, 1]) * 10000
                event_current[NumberOfEvents - 1, 3] = (event_start_mean - max(rawSignal[start:end]))
                event_current[NumberOfEvents - 1, 4] = trapz(rawSignal[start:end], dx=2)
                event_current[NumberOfEvents - 1, 5] = rawSignal[start] - rawSignal[start + 10]
                event_current[NumberOfEvents - 1, 6] = rawSignal[end-1] - rawSignal[end - 11]
                event_current[NumberOfEvents - 1, 7] = (min_index - start) / sampleRate * 1000
                event_current[NumberOfEvents - 1, 8] = (end - min_index) / sampleRate * 1000
                event_current[NumberOfEvents - 1, 9] = (min_index - mean_index_left) / sampleRate * 1000
                event_current[NumberOfEvents - 1, 10] = (mean_index_right - min_index) / sampleRate * 1000
                event_current[NumberOfEvents - 1, 11] = start
                event_current[NumberOfEvents - 1, 12] = end

        # print("stage1 is finished")

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

    print("Accurate Detect Mode")



def detect_events_by_diff(input_signal, sample_rate, min_duration, max_duration):

    if input_signal.ndim != 1:
        raise ValueError('Input signal must be 1D array')

    diff_signal = np.diff(input_signal)
    print( diff_signal[:100])

    b, a = butter(3, 0.05, 'low')
    diff_smoothed = filtfilt(b, a, diff_signal)
    print(diff_smoothed[:100])

    max_pts = find_peaks(diff_smoothed, height=0)[0]
    min_pts = find_peaks(-diff_smoothed, height=0)[0]
    print(max_pts)

    event_starts = input_signal[max_pts]
    event_ends = input_signal[min_pts]

    events = []
    for start, end in zip(event_starts, event_ends):
        if end - start >= min_duration:
            events.append([start, end])

    events = [e for e in events if e[1] - e[0] < max_duration]
    print(events)

    return events


