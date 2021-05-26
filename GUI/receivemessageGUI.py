from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
import receivemessageengine

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui  = MainWindow()
    ui.show()
    #receivemessageengine.label_update()
    sys.exit(app.exec_())
