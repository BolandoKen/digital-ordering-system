import sys
import os
from src.panels.orderHPanel.OrderHPanel import QOrderHPanel
from src.components.Dialogs import QConfirmDialog
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
    QFileDialog,
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
from src.database.Profile import update_name, update_pfp, update_displayname
from src.components.Headers import QProfileNameLabel
from src.components.Dialogs import QChangePfpDialog
from src.components.Buttons import QProfileRadioButton

class QProfileViewState(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.inner_VLayout = QVBoxLayout()
        self.inner_VLayout.setContentsMargins(0,0,0,0)

        self.profileIcon = QProfileImage(None, 150, 150)
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
        self.inner_VLayout.setSpacing(10)

        self.changePfp_dialog = QChangePfpDialog(self.window())

        self.profileIcon = QProfileImage(self.changePfp_dialog.exec, 150, 150, "edit")
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)

        self.changePfp_dialog.set_profileIcon(self.profileIcon)

        self.nameLineEdit = QProfileLineEdit()

        self.displayname_radbtn = QProfileRadioButton("Display Name", self)
        self.resetBtn = QPushButton("reset pin")
        self.resetBtn.clicked.connect(self.handle_resetPin)
        self.resetBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        checkbox_resetFrame = QFrame()
        checkbox_resetFrame.setFixedSize(250, 30)
        checkbox_reset_hbox = QHBoxLayout(checkbox_resetFrame)
        checkbox_reset_hbox.setContentsMargins(0,0,0,0)
        checkbox_reset_hbox.addWidget(self.displayname_radbtn)
        checkbox_reset_hbox.addStretch()
        checkbox_reset_hbox.addWidget(self.resetBtn)

        self.inner_VLayout.addStretch()
        self.inner_VLayout.addWidget(self.nameLineEdit)
        self.inner_VLayout.addWidget(checkbox_resetFrame)
        self.inner_VLayout.addStretch()
        pubsub.subscribe("saveEditProfile", self.saveEditProfile)
        pubsub.subscribe("discardEditProfile", self.discardEditProfile)
        pubsub.subscribe("logout_Event", self.discardEditProfile)
        # have cancel handler, 
        # subscribe on logouts, switch panels, back clicks
        # call cancel on these subscriptions;

  
    def handle_resetPin(self) :
        dialog = QConfirmDialog("Reset PIN", "Are you sure you want to reset your PIN?", self)
        if dialog.exec():
            reset_pin()
            pubsub.publish("logout_Event")

    # handle here saved state
    def discardEditProfile(self, e =None) :
        self.profileIcon.init_profileImg()
        self.nameLineEdit.init_text()
        self.nameLineEdit.setStateInit()
        self.displayname_radbtn.init_checked()
        self.switch(0)

    def saveEditProfile(self, e = None) :
        name = self.nameLineEdit.text()
        dataTuple = (name,)
        error_dict = formValidated(dataTuple, "profile")
        if error_dict["final"] :

            hasImg = self.changePfp_dialog.tempImagePath is not None
            update_name(name)
            if hasImg :
                moveImageToAssets(self.changePfp_dialog.tempImagePath, "profile", "pfp.png")
            update_pfp(hasImg)
            update_displayname(self.displayname_radbtn.isChecked())
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
    





