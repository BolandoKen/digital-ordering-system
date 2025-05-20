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
)

from src.utils.PubSub import pubsub
from src.components.Buttons import QBackButton, QEyeButton, QBongoBtn
from src.components.Dialogs import QSetupPinDialog, QPinDialog
from src.database.queries import ProfileQueries
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QEvent
from src.components.ImageCard import QProfileImage


class QPrinterButton(QBongoBtn) :
    def __init__(self):
        super().__init__()
        self.printer_connected = False
        pubsub.subscribe("printer_connected", self.setPrinterState)
        pubsub.subscribe("printerbtn_clicked", self.setPrinterState_connecting)
        self.clicked.connect(lambda : pubsub.publish("printerbtn_clicked"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        

    def setPrinterState_connecting(self, e = None) :
        if not self.printer_connected :
            self.setState("loading")

    def setPrinterState(self, is_connected) :
        self.printer_connected = is_connected
        if self.printer_connected :
            self.setState("online")
        else :
            self.setState("offline")

class QProfileNameLabel(QLabel) :
    def __init__(self, typeOf = None):
        self.typeOf = typeOf
        super().__init__()
        profilename = ProfileQueries.fetchProfileName()
        finalname = profilename + " - Admin" if self.typeOf == "admin" else profilename
        self.setText(finalname)
        self.setFont(QFont("Helvitica", 15, QFont.Weight.Bold))

        pubsub.subscribe("updateProfile", self.handle_updateProfile)

    def handle_updateProfile(self, e = None) :
        profilename = ProfileQueries.fetchProfileName()
        finalname = profilename + " - Admin" if self.typeOf == "admin" else profilename
        self.setText(finalname)


class QLogoButton(QFrame):
    def __init__(self, pageName):
        super().__init__()
        self.pageName = pageName
        # self.setFixedSize(400, 70)
        self.setStyleSheet("""
            background: transparent;
            padding: 0px;
            color: black;           
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) 

        self.icon_label = QProfileImage(None, 70,70)
        layout.addWidget(self.icon_label)

        self.text_label = QProfileNameLabel(pageName)
        layout.addWidget(self.text_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)
        self.handleDisplayName()
        pubsub.subscribe("updateProfile", self.handleDisplayName)
        self.installEventFilter(self)
        self.icon_label.installEventFilter(self)

    def connectTo(self, callback) :
        self.callback = callback

    
    def eventFilter(self, watched, event) :
        if self.pageName == "admin" or self.pageName == "nocb": return super().eventFilter(watched, event)
        if watched == self or watched == self.icon_label :
            if event.type() == QEvent.Type.MouseButtonPress :
                if event.button() == Qt.MouseButton.LeftButton :
                    self.callback()
        return super().eventFilter(watched, event)

            
    
    def handleDisplayName(self, e = None) :
        self.is_displayname = ProfileQueries.fetchDisplayName() 
        if self.is_displayname :
            self.text_label.show()
        else :
            self.text_label.hide()

class QLogoHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.main_layout = QHBoxLayout(self) 
        self.main_layout.setContentsMargins(0,10,0,10)
        self.setuppin_dialog = QSetupPinDialog(self.window())
        self.pin_dialog = QPinDialog(self.window())
        self.logo = QLogoButton(pageName)
        self.logo.connectTo(self.handleLogoClicked)
        self.main_layout.addWidget(self.logo)
        self.main_layout.addStretch()
        if pageName == "customer" :
            self.logo.connectTo(self.handleLogoClicked)
        if pageName != "admin" :
            self.printerBtn = QPrinterButton()
            self.printerBtn.clicked.connect(lambda: pubsub.publish("printerBtn_clicked"))
            self.main_layout.addWidget(self.printerBtn)



    def handleLogoClicked(self) :
        dialogToExec = self.setuppin_dialog if ProfileQueries.fetchPin() is None else self.pin_dialog
        if dialogToExec.exec() :
            pubsub.publish("login_Event", None)
    
    def updateHeader(self) :
        # update the QLogoButton name or logo/pfp
        pass
    
class QOtherPanelHeader(QFrame) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        # self.main_layout.setContentsMargins(30,10,10,10)
        self.header_layout = QHBoxLayout(self)
        self.headerLabel = QLabel(panelName)
        self.headerLabel.setFont(QFont("Helvetica", 60, QFont.Weight.Bold))
        self.backBtn = QBackButton()
        self.backBtn.clicked.connect(lambda: pubsub.publish("backToFoodPanel_clicked", 0))
        
        self.header_layout.addWidget(self.backBtn)
        self.header_layout.addWidget(self.headerLabel)

        if panelName == "Profile" :
            self.init_ProfilePanel()

    def init_ProfilePanel(self) :
        self.header_layout.addStretch()
        self.editBtn = QPushButton("Edit")
        self.editBtn.setStyleSheet("background-color: white; color: #72CEFF; border-radius: 5px; padding: 5px; font-size: 30x;")
        self.editBtn.clicked.connect(self.handleEditProfile)
        self.cancelBtn = QPushButton("Discard")
        self.cancelBtn.setStyleSheet("background-color: white; color: #C8161D; border-radius: 5px; padding: 5px; font-size: 30px;")
        self.cancelBtn.clicked.connect(self.handleDiscardEdit)
        self.saveBtn = QPushButton("Save")
        self.saveBtn.setStyleSheet("background-color: white; color: #72CEFF; border-radius: 5px; padding: 5px; font-size: 30px;")
        self.saveBtn.clicked.connect(self.handleSaveEdit)
        self.header_layout.addWidget(self.editBtn)
        self.header_layout.addWidget(self.saveBtn)
        self.header_layout.addWidget(self.cancelBtn)
        self.editBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancelBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        pubsub.subscribe("logout_Event", self.handleSaveEdit)
        pubsub.subscribe("updateProfile", self.handleBackToDefaultState)
        pubsub.subscribe("adminPanelSwitched",self.handleDiscardEdit)
        pubsub.subscribe
        self.cancelBtn.hide()
        self.saveBtn.hide()
    
    def handleEditProfile(self) :
        pubsub.publish("editProfile", 1)
        self.editBtn.hide()
        self.cancelBtn.show()
        self.saveBtn.show()
    
    def handleDiscardEdit(self, e=None) :
        pubsub.publish("discardEditProfile")
        self.handleBackToDefaultState()

    def handleSaveEdit(self, e = None) :
        pubsub.publish("saveEditProfile")

    def handleBackToDefaultState(self, e = None) :
        self.editBtn.show()
        self.cancelBtn.hide()
        self.saveBtn.hide()
        

class QFoodPanelHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.pageName = pageName
        self.state = "category"
        pubsub.subscribe(f"{self.pageName}_catCardClicked", self.setHeaderState)
        self.header_layout = QHBoxLayout(self)

        self.backBtn = QBackButton()
 
        self.showUnBtn = QEyeButton()
        showUnBtn_sizePolicy = self.showUnBtn.sizePolicy()
        showUnBtn_sizePolicy.setRetainSizeWhenHidden(True)
        self.showUnBtn.setSizePolicy(showUnBtn_sizePolicy)
        self.showUnavailable = False

        if self.pageName == "admin" : 
            pubsub.subscribe("initHeaderUnBtn_event", self.setShowUnavailableBtn)
        pubsub.subscribe("logout_Event", self.handleBackBtn)
        self.headerLabel = QLabel()
        self.headerLabel.setFont(QFont("Helvetica", 60, QFont.Weight.Bold))

        self.header_layout.addWidget(self.backBtn)
        self.header_layout.addWidget(self.headerLabel)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.showUnBtn)

        self.showUnBtn.clicked.connect(self.handleToggleUnBtn)
        self.backBtn.clicked.connect(self.handleBackBtn)
        self.init_category()

    def init_category(self) :
        if self.pageName == "admin" :
            self.backBtn.hide()
        self.headerLabel.setText("Categories")
        self.showUnBtn.hide()

    def init_food(self) :
        self.backBtn.show()
        self.headerLabel.setText(self.catname)

    def setHeaderState(self, catTuple = None) :
        self.category_id, self.catname = catTuple
        self.state = "food"
        self.init_food()
    
    def handleBackBtn(self, e = None) :
        if self.state == "food" :
            self.state = "category"
            pubsub.publish(f"{self.pageName}_backToCatClicked", None)
            self.init_category()
        elif self.state == "category" :
            pubsub.publish("backBtn_clicked", 1)
    
    def handleToggleUnBtn(self) :
        pubsub.publish(f"admin_toggleShowUnavailable", None)
        self.showUnavailable = not self.showUnavailable
        if self.showUnavailable :
            self.showUnBtn.setState("hide")
        else :
            self.showUnBtn.setState("show")
    
    def setShowUnavailableBtn(self, typeOf) :
        if typeOf == "hide" :
            self.showUnBtn.hide()
        elif typeOf == "show" :
            self.showUnBtn.show()








