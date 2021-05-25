from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
from receivemessageengine import Engine
from time import sleep

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui  = MainWindow()
    ui.show()
    sleep(1)
    Engine.label_update()
    sys.exit(app.exec_())
