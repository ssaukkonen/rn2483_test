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


from Ui_mainwindow import Ui_MainWindow
#import receivemessageengine

class WorkerSignals(QObject):
    signaali = pyqtSignal()

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()

    #@pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        #receivemessageengine().label_update()
        sleep(5)
        self.signals.signaali.emit()
        #self.maxTemp.setText('thread')

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
        worker.signals.signaali.connect(self.test)
        self.threadpool.start(worker)
        #self.update_label()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #self.close()
        self.update_label()

    @pyqtSlot()    
    def test(self):
        self.minTemp.setText('thread')
        
if __name__=="__main__":
    import sys
    app = QApplication([])
    ui  = MainWindow()
    ui.show()
    #receivemessageengine.label_update()
    sys.exit(app.exec_())      
