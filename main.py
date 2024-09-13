# -*- coding : utf-8 -*-
# coding: utf-8
from pyabf import ABF
import os
import eventDetect
import sys
from datetime import datetime

from multiprocessing import Pool
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    path = "data/"
    fileName = os.listdir(path)
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime + '.txt'

    po = Pool(8)

    for i in range(len(fileName)):
        abf = ABF(path + fileName[i])
        current = abf.data[0]
        iterNumber = int(len(current) / (abf.dataRate * 10)) + 1
        if sys.argv[1] == "down":
            for i in range(iterNumber):
                if i != iterNumber - 1:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], 5, 0,
                                    0.99, float(sys.argv[2]), float(sys.argv[3]), resultName, abf.dataRate,))
                else:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[i * abf.dataRate * 10:], 5, 0, 0.99, float(sys.argv[2]), float(sys.argv[3]),
                                    resultName, abf.dataRate,))
        elif sys.argv[1] == "up":
            for i in range(iterNumber):
                if i != iterNumber - 1:
                    po.apply_async(eventDetect.eventUp,
                                   (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], 5, 0,
                                    0.99, float(sys.argv[2]), float(sys.argv[3]), resultName, abf.dataRate,))
                else:
                    po.apply_async(eventDetect.eventUp,
                                   (current[i * abf.dataRate * 10:], 5, 0, 0.99, float(sys.argv[2]), float(sys.argv[3]),
                                    resultName, abf.dataRate,))
        else:
            po.close()
            sys.exit(1)

    po.close()
    po.join()

    print("finish")

