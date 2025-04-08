
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QScrollArea
)

class QScrollAreaLayout(QScrollArea) :
    def __init__(self, QLayout, parentWidget):
        super().__init__()
        self.setWidgetResizable(True)

        self.container = QWidget()
        self.setWidget(self.container)

        self.myLayout = QLayout(self.container)
        parentWidget.addWidget(self)
    
    def addWidget(self, widget) :
        self.myLayout.addWidget(widget)
    
    def addStretch(self) :
        self.myLayout.addStretch()
    
    def getLayout(self) :
        return self.myLayout


