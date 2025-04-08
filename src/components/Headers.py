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


class QFoodPanelHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.pageName = pageName
        self.state = "category"
        pubsub.subscribe(f"{self.pageName}_catCardClicked", self.setHeaderState)
        self.main_layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()
        self.logo = QPushButton("Logo")
        if self.pageName == "customer" :
            self.logo.clicked.connect(self.handleLogoClicked)
        self.main_layout.addWidget(self.logo)
        self.main_layout.addLayout(self.header_layout)
        
        self.backBtn = QPushButton("<-")
        self.showUnBtn = QPushButton("show unavailable items")
 
        self.header = QLabel()
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
        if self.pageName == "admin" :
            self.showUnBtn.show()

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
        self.showUnavailable = False
        pubsub.publish(f"{self.pageName}_toggleShowUnavailable", None)
        self.showUnavailable = not self.showUnavailable
        if self.showUnavailable :
            self.showUnBtn.setText("hide unavailable items") 
        else :
            self.showUnBtn.setText("show unavailable items")

    




