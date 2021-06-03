# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

#from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep

import serial
import io
import binascii
import codecs
import textwrap


from Ui_mainwindow import Ui_MainWindow
#import receivemessageengine

ser = serial.Serial('/dev/ttyS0', 57600)  # open serial port
print(ser.name)         # check which port was really used

class WorkerSignals(QObject):
    #signaali = pyqtSignal()
    current = pyqtSignal(str, str)
    calcData = pyqtSignal(str, str, str, str, str, str)

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        
        global code
        code = str(1234)
        global temp
        global humi
        global date

        komennot = [
            'sys get ver',
            'sys get hweui',
            'radio set wdt 0',
            'mac pause'
        ]
        for m in komennot:
                ser.write(m.encode())
                ser.write(b'\r\n')
                r = ser.readline().decode()
                if len(r):
                    print('\t<<{r}'.format(r=r[:-2]))
                else:
                    print('\t<< no response')

    #@pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        #receivemessageengine().label_update()
        #sleep(5)
        #self.signals.signaali.emit()
        #self.maxTemp.setText('thread')
        self.receive()
        
    def receive(self):
        i=1
        global temp, humi, date
        while i==1:
            #print('start')
            sleep(.2)
            ser.write('radio rx 0'.encode())
            ser.write(b'\r\n')
            #if ser.readable():                
            response = ser.readline().decode()
            if response.startswith('radio_rx'):
                print(response)
                msg2 = response[10:][:-2]
                msg3 = len(msg2)
                print(msg2)
                print(msg3)
                if (((not msg2.endswith('o'))) and (msg3 == 60)) and not msg2.endswith('k'):
                    msg = binascii.unhexlify(msg2.encode()).decode()
                    codeS, temp, humi, date = msg.split(';')               
                    if code == codeS:
                        #print(msg)
                        print(temp, humi, date)
                        self.writeToFile()
                    else:
                            print('wrong code')
                else:
                    print('odd length string')
        else:
            print('loppu')
            
    def writeToFile(self):
        global temp, humi, date
        data = open('../data.txt', 'a')
        data.write('{};{};{}\n'.format(temp, humi, date))
        data.close()
        self.signals.current.emit(temp, humi)
        self.printData()
        

    def printData(self):
        with open('../data.txt') as data:
            sumTemp = 0 # initialize here, outside the loop
            sumHumi = 0
            maxT = 0
            minT = 1000
            maxH = 0
            minH = 100
            count = 0 # and a line counter
            for line in data:
                count += 1 # increment the counter
                data2 = line.split(';')
                #print(data2[0])
                sumTemp += float(data2[0]) # add here, not in a nested loop
                sumHumi += float(data2[1])
                if int(maxT) < int(data2[0]):
                    maxT = (data2[0])
                if int(minT) > int(data2[0]):
                    minT = (data2[0])
                if int(maxH) < int(data2[1]):
                    maxH = (data2[1])
                if int(minH) > int(data2[1]):
                    minH = (data2[1])      
            averageT = round(sumTemp / count, 2)
            averageH = round(sumHumi / count, 2)
            
            
            print(averageT, averageH, maxT, minT, maxH, minH)
            self.signals.calcData.emit(str(averageT), str(averageH), maxT, minT, maxH, minH)
            
            

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #print('mainwindow loppu')
        #self.test()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        #worker = Worker()
        #self.threadpool.start(worker)
        self.testi()
        
    @pyqtSlot()
    def update_label(self):
        print('update_label')
        self.maxTemp.setText('hello')
        self.maxHum.setText('hello2')

    def testi(self):
        worker = Worker()
        worker.signals.current.connect(self.updateCurrent)
        worker.signals.calcData.connect(self.updateData)
        self.threadpool.start(worker)
        #self.update_label()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
        #self.update_label()

    @pyqtSlot()    
    def test(self):
        self.minTemp.setText('thread')
        
    @pyqtSlot(str, str)    
    def updateCurrent(self, temp2, humi2):
        self.curTemp.setText(temp2)
        self.curHum.setText(humi2)

    @pyqtSlot(str, str, str, str, str, str)    
    def updateData(self, averageT2, averageH2, maxT2, minT2, maxH2, minH2):
        self.avgTemp.setText(averageT2)
        self.avgHum.setText(averageH2)
        self.maxTemp.setText(maxT2)
        self.minTemp.setText(minT2)
        self.maxHum.setText(maxH2)
        self.minHum.setText(minH2)
        
if __name__=="__main__":
    import sys
    app = QApplication([])
    ui  = MainWindow()
    ui.show()
    #receivemessageengine.label_update()
    sys.exit(app.exec_())      
