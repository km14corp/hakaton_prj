from pyqt5_plugins.examplebutton import QtWidgets
from window.main_window_new import MainWindow_super

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindow_super()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())