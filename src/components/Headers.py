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
from src.components.Buttons import QBackButton, QLogoButton, QEyeButton
from PyQt6.QtGui import QFont

class QLogoHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.main_layout = QHBoxLayout(self) 
        self.logo = QLogoButton("assets/icons/pfp_icon.svg", "M'sKitchen", pageName)
        self.logo.connectTo(self.handleLogoClicked)
        self.main_layout.addWidget(self.logo)
        self.main_layout.addStretch()
        if pageName == "customer" :
            self.logo.connectTo(self.handleLogoClicked)

    def handleLogoClicked(self) :
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
        self.headerLabel.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        self.header_layout.addWidget(self.headerLabel)

        if panelName == "Profile" :
            self.init_ProfilePanel()

    def init_ProfilePanel(self) :
        self.header_layout.addStretch()
        editBtn = QPushButton("edit")
        editBtn.clicked.connect(self.handleEditProfile)
        self.header_layout.addWidget(editBtn)
    
    def handleEditProfile(self) :
        pubsub.publish("editProfile", None)

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

        self.headerLabel = QLabel()
        self.headerLabel.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        self.header_layout.addWidget(self.backBtn)
        self.header_layout.addWidget(self.headerLabel)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.showUnBtn)

        self.showUnBtn.clicked.connect(self.handleToggleUnBtn)
        self.backBtn.clicked.connect(self.handleBackBtn)
        self.init_category()

    def init_category(self) :
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
    
    def handleBackBtn(self) :
        self.state = "category"
        pubsub.publish(f"{self.pageName}_backToCatClicked", None)
        self.init_category()
    
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








