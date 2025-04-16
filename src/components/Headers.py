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

class QOtherPanelHeader(QFrame) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        self.main_layout = QVBoxLayout(self)
        # self.main_layout.setContentsMargins(30,10,10,10)
        self.main_layout.setSpacing(20)
        self.header_layout = QHBoxLayout()
        self.header = QLabel(panelName)
        self.header.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))
        self.logo = QLogoButton("assets/icons/pfp_icon.svg", "M'sKitchen", "admin")

        self.header_layout.addWidget(self.header)

        self.main_layout.addWidget(self.logo)
        self.main_layout.addLayout(self.header_layout)

        if panelName == "Profile" :
            self.init_ProfilePanel()


    def init_ProfilePanel(self) :
        self.header_layout.addStretch()
        editBtn = QPushButton("edit")
        self.header_layout.addWidget(editBtn)
    
    def handleEdiProfile(self) :
        pass

class QFoodPanelHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.pageName = pageName
        self.state = "category"
        pubsub.subscribe(f"{self.pageName}_catCardClicked", self.setHeaderState)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.header_layout = QHBoxLayout()
        self.logo = QLogoButton("assets/icons/pfp_icon.svg", "M'sKitchen", self.pageName)
        if self.pageName == "customer" :
            self.logo.connectTo(self.handleLogoClicked)

        self.main_layout.addWidget(self.logo)
        self.main_layout.addLayout(self.header_layout)
        
        self.backBtn = QBackButton()
 
        self.showUnBtn = QEyeButton()
        showUnBtn_sizePolicy = self.showUnBtn.sizePolicy()
        showUnBtn_sizePolicy.setRetainSizeWhenHidden(True)
        self.showUnBtn.setSizePolicy(showUnBtn_sizePolicy)
        self.showUnavailable = False

        if self.pageName == "admin" : 
            pubsub.subscribe("initHeaderUnBtn_event", self.setShowUnavailableBtn)

        self.header = QLabel()
        self.header.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        self.header_layout.addWidget(self.backBtn)
        self.header_layout.addWidget(self.header)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.showUnBtn)

        self.showUnBtn.clicked.connect(self.handleToggleUnBtn)
        self.backBtn.clicked.connect(self.handleBackBtn)
        self.init_category()

    def init_category(self) :
        self.backBtn.hide()
        self.header.setText("Categories")
        self.showUnBtn.hide()

    def init_food(self) :
        self.backBtn.show()
        self.header.setText(self.catname)

    def setHeaderState(self, catTuple = None) :
        self.category_id, self.catname = catTuple
        self.state = "food"
        self.init_food()
    
    def handleBackBtn(self) :
        self.state = "category"
        pubsub.publish(f"{self.pageName}_backToCatClicked", None)
        self.init_category()
    
    def handleLogoClicked(self) :
        pubsub.publish("login_Event", None)
    
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








