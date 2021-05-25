#from PyQt5.QtWidgets import QMainWindow
from ui.mainwindow import MainWindow

class Engine():
#def test(self):
#   self.maxTemp.setText('11')
    def label_update():
        print('label_update')
        MainWindow().update_label()
