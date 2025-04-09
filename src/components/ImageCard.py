from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog
)
from src.components.Buttons import QImageButton
from PyQt6.QtGui import QPixmap

class QSelectImageCard(QFrame) :
    def __init__(self, handleClearBtnCallback):
        super().__init__()
        self.callback = handleClearBtnCallback
        self.imageCard_layout = QVBoxLayout(self)
        self.clearButton = QPushButton("X")
        self.clearButton.clicked.connect(self.clearImg)
        self.imageButton = QImageButton("+")
        self.imageCard_layout.addWidget(self.clearButton)
        self.imageCard_layout.addWidget(self.imageButton)

    def connectTo(self, callback) :
        self.imageButton.connectTo(callback)
    
    def clearImg(self) :
        self.imageButton.setPixmap(QPixmap()) # set to default pixmap
        self.imageButton.setText("+")
        self.callback()


    def getLabel(self) :
        return self.imageButton

