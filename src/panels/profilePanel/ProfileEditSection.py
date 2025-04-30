import sys
import os
from src.panels.orderHPanel.OrderHPanel import QOrderHPanel

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
    QVBoxLayout,
    QScrollArea,
    QLineEdit,
    QFileDialog
)
from src.utils.PixMap import setPixMapOf
from src.utils.PubSub import pubsub
from PyQt6.QtCore import Qt
from src.database.Profile import reset_pin
from src.components.ImageCard import QProfileImage
from src.utils.PixMap import checkImgSize, saveImageToLocalTemp, setPixMapOf, moveImageToAssets
from src.database.queries import ProfileQueries
from src.components.LineEdit import QProfileLineEdit
from src.utils.FormValid import formValidated
from src.database.Profile import update_name
from src.components.Headers import QProfileNameLabel

class QProfileViewState(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.inner_VLayout = QVBoxLayout()
        self.inner_VLayout.setContentsMargins(0,0,0,0)
        self.profileIcon = QProfileImage()
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)

        self.profilename_label = QProfileNameLabel()
        self.inner_VLayout.addWidget(self.profilename_label)

class QProfileEditState(QFrame) : 
    def __init__(self, switch):
        super().__init__()
        self.switch = switch
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.inner_VLayout = QVBoxLayout()
        self.inner_VLayout.setContentsMargins(0,0,0,0)
        self.profileIcon = QProfileImage()
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)

        self.changeBtn = QPushButton("change")
        self.changeBtn.clicked.connect(self.open_file)
        self.changeBtn.setFixedWidth(100)
        self.nameLineEdit = QProfileLineEdit()

        self.checkbox = QPushButton("O")
        self.checkbox.setFixedWidth(30)
        self.resetBtn = QPushButton("reset pin")
        self.resetBtn.clicked.connect(self.handle_resetPin)
        
        checkbox_resetFrame = QFrame()
        checkbox_resetFrame.setFixedWidth(250)
        checkbox_resetFrame.setFixedSize(250, 30)
        checkbox_reset_hbox = QHBoxLayout(checkbox_resetFrame)
        checkbox_reset_hbox.setContentsMargins(0,0,0,0)
        checkbox_reset_hbox.addWidget(self.checkbox)
        checkbox_reset_hbox.addStretch()
        checkbox_reset_hbox.addWidget(self.resetBtn)


        self.inner_VLayout.addWidget(self.changeBtn)
        self.inner_VLayout.addWidget(self.nameLineEdit)
        self.inner_VLayout.addWidget(checkbox_resetFrame)
        pubsub.subscribe("saveProfile", self.saveProfile)

    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            print(checkImgSize(file_path)) #check for filesize bfore compress, no
            self.tempImagePath = saveImageToLocalTemp(file_path, "temp.png")
            setPixMapOf(self.profileIcon, "temp.png", "temp")  

    def handle_resetPin(self) :
        reset_pin()
        pubsub.publish("logout_Event")
        self.saveProfile()

    # handle here saved state
    def saveProfile(self, e = None) :
        name = self.nameLineEdit.text()
        dataTuple = (name,)
        error_dict = formValidated(dataTuple, "profile")
        if error_dict["final"] :
            update_name(name)
            pubsub.publish("updateProfile")
            self.switch(0)
        else :
            self.nameLineEdit.setStateInvalid(error_dict["profile_name"])


class QProfile(QStackedWidget) :
    def __init__(self):
        super().__init__()
        self.viewState = QProfileViewState()
        self.editState = QProfileEditState(self.switch)
        self.addWidget(self.viewState)
        self.addWidget(self.editState)
        self.curr = 0
        pubsub.subscribe("editProfile", self.switch)

    def switch(self, index) :
        self.setCurrentIndex(index)
    





