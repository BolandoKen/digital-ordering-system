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