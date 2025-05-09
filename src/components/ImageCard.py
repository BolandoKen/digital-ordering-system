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
    QFileDialog,
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect
)
from src.components.Buttons import QCloseButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from src.utils.PixMap import setPixMapOf
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize
from src.utils.PubSub import pubsub
from src.database.queries import ProfileQueries

class QImageButton(QLabel) :
    def __init__(self, text) :
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()

class QSelectImageCard(QFrame) :
    def __init__(self, handleClearBtnCallback):
        super().__init__()
        self.setObjectName("imageCard")
        self.setStyleSheet("#imageCard{border: 2px solid #D9D9D9; border-radius: 10px; padding-bottom: 25px}")
        self.callback = handleClearBtnCallback
        self.imageCard_layout = QVBoxLayout(self)
        self.clearButton = QCloseButton()
        self.clearButton.setFixedWidth(20)
        self.clearButton.hide()

        closepolicy = self.clearButton.sizePolicy()
        closepolicy.setRetainSizeWhenHidden(True)
        self.clearButton.setSizePolicy(closepolicy)

        self.clearButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clearButton.clicked.connect(self.clearImg)
        self.imageButton = QImageButton("+")
        self.imageCard_layout.addWidget(self.clearButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.imageCard_layout.addWidget(self.imageButton)
        setPixMapOf(self.imageButton, "addCircle.svg", "icon")
        # self.imageButton.setFixedSize(150,150)
        # self.imageButton.setScaledContents(True)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(128,128,128, 100))
        self.setGraphicsEffect(shadow)

        self.imageButton.setFixedSize(200,200)
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


class QCatLabelImageFrame(QFrame) :
    def __init__(self, name, imgfile, panelName) :
        super().__init__()
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(0,0,0,0)
        self.name = name
        self.imgfile = imgfile
        self.panelName = panelName
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setMaximumWidth(250)
        self.nameLabel.setStyleSheet("""
                    background-color: transparent;
                    color: black;
                    font-size: 40px;
                    font: "Helvetica";
                    font-weight: 650;
                    margin-left: 10px;
                    """)
        self.imgWidget = QLabel()
        setPixMapOf(self.imgWidget, self.imgfile, "category")

        self.hbox.addWidget(self.nameLabel)
        self.hbox.addStretch()
        self.hbox.addWidget(self.imgWidget)    
        self.hbox.addStretch()


class QProfileImage(QLabel) :
    def __init__(self, cb = None, width = None, height = None, typeOf = None):
        super().__init__()
        self.width = width
        self.height = height
        self.imgfile = None
        self.typeOf = typeOf
        self.init_profileImg()
        self.cb = cb 
        pubsub.subscribe("updateProfile", self.init_profileImg)

        if typeOf == "edit" :
            self.editMask = QEditMask(self)
            self.editMask.setFixedSize(width,height)
            self.editMask.editLabelIcon.clicked.connect(self.cb) # dirty workaround for handling clicked on the icon; should have done transparent
            self.editMask.move(0,0)
            self.editMask.hide()
    

    def enterEvent(self, event):
        if self.typeOf == "edit" :
            self.editMask.show()
        return super().enterEvent(event)

    def leaveEvent(self, a0):
        if self.typeOf == "edit" :
            self.editMask.hide()
        return super().leaveEvent(a0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.cb is not None:
            self.cb()

    def init_profileImg(self, e= None) :
        self.imgfile = ProfileQueries.fetchProfileImg()
        imgfilepath = setPixMapOf(self, self.imgfile, "profile")["path"]
        if self.width is not None and self.height is not None : # set fixed size for qprofileimage with set width/height parameters
            self.setFixedSize(self.width, self.height)
            self.setScaledContents(True)
        return imgfilepath # whats this for? idk
    
    def clearImg(self) :
        setPixMapOf(self, None, "profile")

class QEditMask(QFrame) :
    def __init__(self, parent = None) :
        super().__init__(parent)  
        self.setStyleSheet("background-color: rgba(128, 128, 128, 76);")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        opacity_effect2 = QGraphicsOpacityEffect()
        opacity_effect2.setOpacity(1) 
        self.editLabelIcon = QPushButton()
        self.editLabelIcon.setStyleSheet("background-color: transparent; border: none;")
        icon = QIcon("assets/icons/edit_icon2.svg")        
        self.editLabelIcon.setIcon(icon)
        self.editLabelIcon.setIconSize(QSize(50,50))

        self.editLabelIcon.setGraphicsEffect(opacity_effect2) 
        self.main_layout.addWidget(self.editLabelIcon, alignment=Qt.AlignmentFlag.AlignCenter)