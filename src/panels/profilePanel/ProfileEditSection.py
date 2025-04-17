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
)
from src.utils.PixMap import setPixMapOf
from src.utils.PubSub import pubsub
from PyQt6.QtCore import Qt

class QProfileViewState(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.inner_VLayout = QVBoxLayout()
        self.inner_VLayout.setContentsMargins(0,0,0,0)
        self.profileIcon = QLabel()
        setPixMapOf(self.profileIcon, "pfp_icon.svg", "icon")
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)
        self.inner_VLayout.addWidget(QLabel("M's Kitchen"))


class QProfileEditState(QFrame) : 
    def __init__(self, switch):
        super().__init__()
        self.switch = switch
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.inner_VLayout = QVBoxLayout()
        self.inner_VLayout.setContentsMargins(0,0,0,0)
        self.profileIcon = QLabel()
        setPixMapOf(self.profileIcon, "pfp_icon.svg", "icon")
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)

        self.changeBtn = QPushButton("change")
        self.changeBtn.setFixedWidth(100)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setFixedSize(250,50)
        self.checkbox = QPushButton("O")
        self.checkbox.setFixedWidth(30)
        self.inner_VLayout.addWidget(self.changeBtn)
        self.inner_VLayout.addWidget(self.nameLineEdit)
        self.inner_VLayout.addWidget(self.checkbox)
        pubsub.subscribe("saveProfile", self.saveProfile)

    # handle here saved state
    def saveProfile(self, e = None) :
        self.switch(0)


    

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
    





