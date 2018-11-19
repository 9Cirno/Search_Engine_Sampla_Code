import sys
from PyQt4 import QtGui, QtCore


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):


        self.btn2 = QtGui.QPushButton("Button 2", self)
        self.btn2.move(150, 50)
        self.btn2.clicked.connect(self.buttonClicked)

        self.results_browser = QtGui.QTextEdit(self)
        self.results_browser.resize(300,300)
        self.results_browser.move(30,80)
        self.results_browser.setText(' was pressed')

        self.input = QtGui.QTextEdit(self)
        self.input.move(30,50)

        self.statusBar()

        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):

        text = self.input.toPlainText()
        self.results_browser.setText(text)

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
