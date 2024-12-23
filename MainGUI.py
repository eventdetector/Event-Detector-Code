# coding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QMenu
from matplotlib import patches
from pyqt5_plugins.examplebutton import QtWidgets

# from eventsDetectGUI import Ui_MainWindow
from testchajian import Ui_MainWindow
from Function import detectMainAccurate, detectMainFast
from multiprocessing import freeze_support
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import Qt
import frozen
import pyabf
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.style as mplStyle
import pandas as pd
import numpy as np

from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)

try:
    # Only exists on Windows.
    from ctypes import windll
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    freeze_support()


    class MyMainWindow(QMainWindow, Ui_MainWindow):
        def __init__(self, parent=None):
            super(MyMainWindow, self).__init__(parent)
            self.setupUi(self)
            mplStyle.use("classic")#使用样式，必须在绘图之前调用,修改字体后才可显示汉字
            #设置窗口名称和图标
            self.setWindowTitle("EZ")
            # self.setWindowIcon(QIcon(':/logo.ico'))
            self.lineEdit_pattern.setText("down")
            self.lineEdit_startCoeff.setText("5")
            self.lineEdit_endCoeff.setText("0")
            self.lineEdit_filterCoeff.setText("0.99")
            self.lineEdit_minDuration.setText("0")
            self.lineEdit_maxDuration.setText("10")
            self.lineEdit_window.setText("1024")
            self.lineEdit_buffer.setText("100")
            self.lineEdit_step.setText("1024")
            self.pushButton_selectFile.clicked.connect(self.getFile)
            self.pushButton_start.clicked.connect(self.detect)
            self.pushButton_start.clicked.connect(self.creat_table_show) #以表格的形式显示内容
            plt.style.use('fast')
            self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
            self.addToolBar(NavigationToolbar(self.MplWidget2.canvas, self))
            # self.textBrowser.setFixedWidth(1000)
            # self.textBrowser.setText("The results are displayed here")
            # 添加右键菜单
            self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

            #双模式
            self.comboBox = self.findChild(QtWidgets.QComboBox, 'comboBox_2')
            #self.comboBox.currentIndexChanged.connect(self.combo_changed)  # 绑定事件


        def showABF(self,fileList):

            # abf_file_path = "normal_110mv_pH8_YH_11_0000.abf"
            abf_file_path =fileList
            abf = pyabf.ABF(abf_file_path)
            for sweep in range(abf.sweepCount):
                abf.setSweep(sweep)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(abf.sweepX, abf.sweepY, linewidth=0.3,color="black")

            self.MplWidget.canvas.axes.tick_params(axis='x', labelsize=10)
            self.MplWidget.canvas.axes.tick_params(axis='y', labelsize=10)
            self.MplWidget.canvas.axes.set_xlabel('Time (s)', fontsize=10, labelpad=1)
            self.MplWidget.canvas.axes.set_ylabel('Current (pA)', fontsize=10, labelpad=1)
            self.MplWidget.canvas.figure.subplots_adjust(left=0.1, bottom=0.2, wspace=0.3)
            self.MplWidget.canvas.draw()



        def getFile(self):
            fileNames, _ = QFileDialog.getOpenFileNames(self, 'Select File', 'C:\\Users\\涂图\\Desktop\\abf文件',
                                                        "Axon Binary File(*.abf)")
            fileList = ';'.join(fileNames)
            global filepath
            filepath=fileList  
            self.textBrowser_fileName.setPlainText(fileList)
            #show the fiture
            self.showABF(fileList)


        def detect(self, resultPath=None):
            #获取当前选中的模式
            selected_mode=self.comboBox.currentIndex()

            global path_openfile_name
            pattern = self.lineEdit_pattern.text()
            startCoeff = int(self.lineEdit_startCoeff.text())
            endCoeff = int(self.lineEdit_endCoeff.text())
            filterCoeff = float(self.lineEdit_filterCoeff.text())
            minDuration = float(self.lineEdit_minDuration.text())
            maxDuration = float(self.lineEdit_maxDuration.text())
            windowSize=int(self.lineEdit_window.text())
            bufferSize = int(self.lineEdit_buffer.text())
            stepSize=int(self.lineEdit_step.text())
            fileNames = self.textBrowser_fileName.toPlainText()
            fileList = fileNames.split(";")
            if fileList == ['']:
                self.showNoFileErrorMessageBox()
            else:
                if selected_mode == 0 :
                    resultPath = detectMainFast(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration)
                    path_openfile_name=resultPath
                    print(path_openfile_name)
                    print("执行快速模式")
                # self.textBrowser.setText(resultContent)
                else:
                    resultPath = detectMainAccurate(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,windowSize,bufferSize,stepSize)
                    path_openfile_name = resultPath
                    print(path_openfile_name)
                    print("执行精确模式")

        def showNoFileErrorMessageBox(self):
            QMessageBox.critical(self, "NoFileError", "Please select files before detecting", )

        def creat_table_show(self):
            if len(path_openfile_name) > 0:
                input_table = pd.read_excel(path_openfile_name)
                input_table_rows = input_table.shape[0]
                input_table_colunms = input_table.shape[1]
                input_table_header = input_table.columns.values.tolist()

                self.tableWidget.setColumnCount(input_table_colunms)
                self.tableWidget.setRowCount(input_table_rows)
                self.tableWidget.setHorizontalHeaderLabels(input_table_header)

                for i in range(input_table_rows):
                    input_table_rows_values = input_table.iloc[[i]]
                    input_table_rows_values_array = np.array(input_table_rows_values)
                    input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                    for j in range(input_table_colunms):
                        input_table_items_list = input_table_rows_values_list[j]

                        input_table_items = str(input_table_items_list)
                        newItem = QTableWidgetItem(input_table_items)
                        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tableWidget.setItem(i, j, newItem)

            else:
                self.centralWidget.show()

        # 新添加的槽函数
        def generateMenu(self, pos):
            selected_rows = [index.row() for index in self.tableWidget.selectionModel().selectedRows()]
            if selected_rows:
                menu = QMenu()
                item1 = menu.addAction(u"show")
                action = menu.exec_(self.tableWidget.mapToGlobal(pos))
                if action == item1:
                    for row_num in selected_rows:
                        start_point = int(float(self.tableWidget.item(row_num, 0).text()))
                        end_point = int(float(self.tableWidget.item(row_num, 1).text()))
                        self.showPartABF(start_point - 5, end_point)  #从开始点前五个点开始展示
            else:
                return

        def showPartABF(self, start_point, end_point):
            abf_file_path = filepath
            # abf_file_path = fileList
            abf = pyabf.ABF(abf_file_path)
            for sweep in range(abf.sweepCount):
                abf.setSweep(sweep)
            self.MplWidget2.canvas.axes.clear()
            self.MplWidget2.canvas.axes.plot(abf.sweepX[start_point:end_point], abf.sweepY[start_point:end_point],
                                            linewidth=2, color='black')
            self.MplWidget2.canvas.axes.tick_params(axis='x', labelsize=10)
            self.MplWidget2.canvas.axes.tick_params(axis='y', labelsize=10)
            self.MplWidget2.canvas.axes.set_xlabel('Time (s)', fontsize=10, labelpad=1)
            self.MplWidget2.canvas.axes.set_ylabel('Current (pA)', fontsize=10, labelpad=1)
            self.MplWidget2.canvas.figure.subplots_adjust(left=0.1, bottom=0.2, wspace=0.3)
            self.MplWidget2.canvas.draw()

            # Draw the red rectangle around the specified data range
            # self.MplWidget.canvas.axes.clear() 
            self.MplWidget.canvas.axes.plot(abf.sweepX, abf.sweepY, linewidth=0.3, color="grey")
            rect_x = abf.sweepX[start_point]
            rect_width = abf.sweepX[end_point] - abf.sweepX[start_point]
            rect_ymin = min(abf.sweepY[start_point:end_point])
            rect_ymax = max(abf.sweepY[start_point:end_point])
            rect_height = rect_ymax - rect_ymin
            rect = patches.Rectangle((rect_x, rect_ymin), rect_width, rect_height, linewidth=1, edgecolor='r',
                                     facecolor='none')
            self.MplWidget.canvas.axes.add_patch(rect)
            self.MplWidget.canvas.axes.tick_params(axis='x', labelsize=10)
            self.MplWidget.canvas.axes.tick_params(axis='y', labelsize=10)
            self.MplWidget.canvas.axes.set_xlabel('Time (s)', fontsize=10, labelpad=1)
            self.MplWidget.canvas.axes.set_ylabel('Current (pA)', fontsize=10, labelpad=1)
            self.MplWidget.canvas.figure.subplots_adjust(left=0.1, bottom=0.2, wspace=0.3)
            self.MplWidget.canvas.draw()


    app = QApplication([])
    app.setWindowIcon(QIcon('D:\Code\PycharmProjects\easynanopore\logo.ico'))

    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
