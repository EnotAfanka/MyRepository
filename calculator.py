import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from functools import partial


errorMessage = 'ERROR'


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setMinimumSize(235, 300)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setStyleSheet("background-color: #222222;")
        self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.generalLayout = QVBoxLayout()
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()
        if screenWidth < 500:
            self.setGeometry(0, 0, int(screenWidth * 0.9), int(screenHeight * 0.7))
        else:
            self.setGeometry(0, 0, 300, 400)
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setMinimumSize(40, 100)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet('QLineEdit {border: 1px solid #B2DFDB; font-size: 32px; font-weight: bold; background-color: #B2DFDB; box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);}' )
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ['7', '8', '9', '/', '('],
            ['4', '5', '6', '*', ')'],
            ['1', '2', '3', '-', 'C'],
            ['0', '00', '.', '+', '=']
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setMinimumSize(40, 40)
                self.buttonMap[key].setStyleSheet(
                    'QPushButton {background-color: #B2DFDB; color: black; padding: 5px; border: 2px solid gray; border-radius: 20px; font-size: 18px;}'
                    'QPushButton:hover {background-color: #80CBC4;}'
                    'QPushButton:pressed {border-style: inset; background-color: #4DB6AC;}'
                )
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.buttonMap['C'].setStyleSheet(
                    'QPushButton {background-color: #ff8c69; color: black; padding: 5px; border: 2px solid gray; border-radius: 20px; font-size: 18px;}'
                    'QPushButton:hover {background-color: #ff7f7f;}'
                    'QPushButton:pressed {border-style: inset; background-color: #ff4040;}'
                )

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')


def evaluate(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = errorMessage
    return result


class CalculatorFunction:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == errorMessage:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {'=', 'C'}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        self._view.buttonMap['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap['C'].clicked.connect(self._view.clearDisplay)


def main():
    calcapp = QApplication([])
    calcwindow = CalculatorWindow()
    calcwindow.show()
    CalculatorFunction(model=evaluate, view=calcwindow)
    sys.exit(calcapp.exec())


if __name__ == '__main__':
    main()
