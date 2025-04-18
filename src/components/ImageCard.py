from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
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
from src.utils.PixMap import setPixMapOf
from PyQt6.QtCore import Qt

class QSelectImageCard(QFrame) :
    def __init__(self, handleClearBtnCallback):
        super().__init__()
        self.setObjectName("imageCard")
        self.setStyleSheet("#imageCard{border: 1px solid black; border-radius: 10px}")
        self.callback = handleClearBtnCallback
        self.imageCard_layout = QVBoxLayout(self)
        self.clearButton = QPushButton("X")
        self.clearButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clearButton.clicked.connect(self.clearImg)
        self.imageButton = QImageButton("+")
        self.imageCard_layout.addWidget(self.clearButton)
        self.imageCard_layout.addWidget(self.imageButton)
        setPixMapOf(self.imageButton, "addCircle.svg", "icon")
        self.imageButton.setFixedSize(125,125)

    def connectTo(self, callback) :
        self.imageButton.connectTo(callback)
    
    def clearImg(self) :
        setPixMapOf(self.imageButton, "addCircle.svg", "icon")
        self.callback()


    def getLabel(self) :
        return self.imageButton


class QImageLabel(QLabel) :
    def __init__(self, imgfile):
        super().__init__()
        setPixMapOf(self, imgfile, "icon")


class QCatLabelImageLayout(QHBoxLayout) :
    def __init__(self, name, imgfile, panelName) :
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.name = name
        self.imgfile = imgfile
        self.panelName = panelName
        self.nameLabel = QLabel(self.name)
        self.imgWidget = QLabel()
        setPixMapOf(self.imgWidget, self.imgfile, "category")

        self.addWidget(self.nameLabel)
        self.addWidget(self.imgWidget)                