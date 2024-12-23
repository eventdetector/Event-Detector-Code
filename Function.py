from pyabf import ABF
import os
# import eventDetectTest
# from eventDetectTest import eventDownFast
# from eventDetectTest import eventUpFast
#import eventDetect
from eventDetect import eventDownFast
# from eventDetect import eventUpFast
from eventDetectAccurate import eventDownAccurate
from datetime import datetime
import sys
import time
import pandas as pd

from multiprocessing import Pool


def detectMainAccurate(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,windowSize,bufferSize,stepSize):
    # 
    # start_time = time.perf_counter()
    # fileName = fileList
    # nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # if not os.path.exists('result/'):
    #     os.makedirs('result/')
    # resultName = 'result/' + nowTime + '.txt'
    #
    # po = Pool(8)
    # fileNumber = 0
    #
    # for i in range(len(fileName)):
    #     abf = ABF(fileName[i])
    #     fileNumber += 1
    #     current = abf.data[0]
    #     iterNumber = int(len(current) / (abf.dataRate * 10)) + 1
    #     if (pattern == "down") or (pattern == "DOWN"):
    #         for i in range(iterNumber):
    #             if i == 0:
    #                 po.apply_async(eventDetect.eventDownFast,
    #                                (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff, endCoeff,
    #                                 filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
    #             elif i != iterNumber - 1:
    #                 po.apply_async(eventDetect.eventDownFast,
    #                                (current[i * abf.dataRate * 10 - 1000:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff, endCoeff,
    #                                 filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
    #             else:
    #                 po.apply_async(eventDetect.eventDownFast,
    #                                (current[i * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
    #                                 resultName, abf.dataRate, fileNumber, i,))
    #     # elif (pattern == "up") or (pattern == "UP"):
    #     #     for i in range(iterNumber):
    #     #         if i == 0:
    #     #             po.apply_async(eventDetect.eventUpFast,
    #     #                            (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff,
    #     #                            endCoeff, filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
    #     #         elif i != iterNumber - 1:
    #     #             po.apply_async(eventDetect.eventUpFast,
    #     #                            (current[i * abf.dataRate * 10 - 1000:i * abf.dataRate * 10 + abf.dataRate * 10],
    #     #                             startCoeff, endCoeff,
    #     #                             filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
    #     #         else:
    #     #             po.apply_async(eventDetect.eventUpFast,
    #     #                            (current[i * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
    #     #                             resultName, abf.dataRate, fileNumber, i,))
    #     else:
    #         po.close()
    #         sys.exit(1)
    #
    # po.close()
    # po.join()
    #
    # print(resultName)
    # # time.sleep(5)  # wait for 5 seconds
    # with open(resultName, 'r') as f:
    #     resultContent = f.read()
    #
    #  
    # column_names = ["Start point", "End point", "Time of duration", "Current amplitude", "Baseline",
    #                 "Amplitude/Baseline*10000",
    #                 "Baseline to event peak amplitude(pA)",
    #                 "Baseline to event minimum amplitude", "Signal area", "Signal left slope", "Signal right slope",
    #                 "Front full peak width(ms)",
    #                 "After full peak width(ms)",
    #                 "First half peak width(ms)", "Back half peak width(ms)"]
    # 
    # df = pd.read_csv(resultName, delimiter='\t', names=column_names)
    # 
    # excel_path = 'result/' + nowTime + '.xlsx'
    # df.to_excel(excel_path, index=False)
    #
    # elapsed = (time.perf_counter() - start_time)
    # print("Time used:", elapsed)
    # print('finish')
    # return excel_path

    
    start_time = time.perf_counter()
    fileName = fileList
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime +'Accurate'+ '.txt'

    po = Pool(8)
    fileNumber = 0
    abf = ABF(fileName[0])
    current = abf.data[0]
    if (pattern == "down") or (pattern == "DOWN"):
        eventDownAccurate(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber,windowSize,bufferSize,stepSize)
    with open(resultName, 'r') as f:
        resultContent = f.read()

    column_names = ["Start point", "End point", "Time of duration", "Current amplitude", "Baseline",
                    "Amplitude/Baseline*10000",
                    "Baseline to event peak amplitude(pA)",
                    "Baseline to event minimum amplitude", "Signal area", "Signal left slope", "Signal right slope",
                    "Front full peak width(ms)",
                    "After full peak width(ms)",
                    "First half peak width(ms)", "Back half peak width(ms)"]

    df = pd.read_csv(resultName, delimiter='\t', names=column_names)

    excel_path = 'result/' + nowTime+'Accurate' + '.xlsx'
    df.to_excel(excel_path, index=False)

    elapsed = (time.perf_counter() - start_time)
    print("Time used:", elapsed)
    print('finish')
    return excel_path 
def detectMainFast(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration):
    
    start_time = time.perf_counter()
    fileName = fileList
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime +'Fast'+ '.txt'

    po = Pool(8)
    fileNumber = 0
    abf = ABF(fileName[0])
    current = abf.data[0]
    if (pattern == "down") or (pattern == "DOWN"):
        eventDownFast(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber)
    with open(resultName, 'r') as f:
        resultContent = f.read()


    column_names = ["Start point", "End point", "Time of duration", "Current amplitude", "Baseline",
                    "Amplitude/Baseline*10000",
                    "Baseline to event peak amplitude(pA)",
                    "Baseline to event minimum amplitude", "Signal area", "Signal left slope", "Signal right slope",
                    "Front full peak width(ms)",
                    "After full peak width(ms)",
                    "First half peak width(ms)", "Back half peak width(ms)"]

    df = pd.read_csv(resultName, delimiter='\t', names=column_names)

    excel_path = 'result/' + nowTime  +'Fast'+ '.xlsx'
    df.to_excel(excel_path, index=False)

    elapsed = (time.perf_counter() - start_time)
    print("Time used:", elapsed)
    print('finish')
    return excel_path 

def detectMainFast2(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration):
    start_time= time.perf_counter()
    fileName = fileList
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime + '.txt'

    po = Pool(8)
    fileNumber = 0

    for i in range(len(fileName)):
        abf = ABF(fileName[i])
        fileNumber += 1
        current = abf.data[0]
        iterNumber = int(len(current) / (abf.dataRate * 10)) + 1
        if (pattern == "down") or (pattern == "DOWN"):
            for j in range(iterNumber):
                if j == 0:
                    po.apply_async(eventDetect.eventDownFast,
                                   (
                                   current[j * abf.dataRate * 10:j * abf.dataRate * 10 + abf.dataRate * 10], startCoeff,
                                   endCoeff,
                                   filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, j,))
                elif j != iterNumber - 1:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[j * abf.dataRate * 10 - 1000:j * abf.dataRate * 10 + abf.dataRate * 10],
                                    startCoeff, endCoeff,
                                    filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, j,))
                else:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[j * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration,
                                    maxDuration,
                                    resultName, abf.dataRate, fileNumber, j,))
        elif (pattern == "up") or (pattern == "UP"):
            for j in range(iterNumber):
                if j == 0:
                    po.apply_async(eventDetect.eventUpFast,
                                   (
                                   current[j * abf.dataRate * 10:j * abf.dataRate * 10 + abf.dataRate * 10], startCoeff,
                                   endCoeff, filterCoeff, minDuration, maxDuration, resultName, abf.dataRate,
                                   fileNumber, j,))
                elif j != iterNumber - 1:
                    po.apply_async(eventDetect.eventUpFast,
                                   (current[j * abf.dataRate * 10 - 1000:j * abf.dataRate * 10 + abf.dataRate * 10],
                                    startCoeff, endCoeff,
                                    filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, j,))
                else:
                    po.apply_async(eventDetect.eventUpFast,
                                   (current[j * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration,
                                    maxDuration,
                                    resultName, abf.dataRate, fileNumber, j,))
        else:
            po.close()
            sys.exit(1)

    po.close()
    po.join()

    column_names = ["Start point", "End point", "Time of duration", "Current amplitude", "Baseline",
                    "Amplitude/Baseline*10000",
                    "Baseline to event peak amplitude(pA)",
                    "Baseline to event minimum amplitude", "Signal area", "Signal left slope", "Signal right slope",
                    "Front full peak width(ms)",
                    "After full peak width(ms)",
                    "First half peak width(ms)", "Back half peak width(ms)"]

    df = pd.read_csv(resultName, delimiter='\t', names=column_names)

    excel_path = 'result/' + nowTime + '.xlsx'
    df.to_excel(excel_path, index=False)

    elapsed = (time.perf_counter() - start_time)
    print("Time used:", elapsed)
    print('finish')
    return excel_path 
def detectMain(pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration):
    path = "data/"
    fileName = os.listdir(path)
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime + '.txt'

    for i in range(len(fileName)):
        abf = ABF(path + fileName[i])
        current = abf.data[0]
        if pattern == "down":
            eventDownFast(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
                          resultName,
                          abf.dataRate)
        elif pattern == "up":
            eventUpFast(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
                        resultName,
                        abf.dataRate)
        else:
            sys.exit(1)

    print('finish')
