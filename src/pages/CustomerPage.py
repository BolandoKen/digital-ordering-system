from src.panels.foodPanel.FoodPanel import QFoodPanel
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
    QGridLayout,
)
from src.components.SideBar import QCustomerSideBar
from src.components.Headers import QLogoHeader

from src.utils.PubSub import pubsub
from src.components.Buttons import QDineInButton, QTakeOutButton, QLogoButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt



class QCustomerPage(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.customerPage_stackedWidgets = QStackedWidget()

        self.customerFoodMenuPanel = QCustomerFoodMenuPanel(self.customerPage_stackedWidgets)
        self.customerGreetPanel = QCustomerGreetPanel(self.customerPage_stackedWidgets)
        self.customerConfirmOrderPanel = QCustomerConfirmOrderPanel(self.customerPage_stackedWidgets)
        self.customerPrintingPanel = QCustomerPrintingPanel(self.customerPage_stackedWidgets)
        # self.main_layout.addWidget(self.customerFoodMenuPanel)
        self.customerPage_stackedWidgets.addWidget(self.customerFoodMenuPanel)
        self.customerPage_stackedWidgets.addWidget(self.customerGreetPanel)
        self.customerPage_stackedWidgets.addWidget(self.customerConfirmOrderPanel)
        self.customerPage_stackedWidgets.addWidget(self.customerPrintingPanel)
        
        self.main_layout.addWidget(self.customerPage_stackedWidgets)
        self.customerPage_stackedWidgets.setCurrentIndex(1)


        
        
class QCustomerFoodMenuPanel(QFrame) :
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.objectName = "customer"
        self.foodPanel = QFoodPanel(self.objectName)
        self.sideBar = QCustomerSideBar()
        self.logoHeader = QLogoHeader("customer")
        self.customer_layout = QGridLayout(self)
        self.customer_layout.setSpacing(0)
        self.customer_layout.setContentsMargins(0,0,0,0)
        self.customer_layout.addWidget(self.logoHeader, 0,0)
        self.customer_layout.addWidget(self.foodPanel, 1, 0)
        self.customer_layout.addWidget(self.sideBar, 0, 1, 2, 1)

class QCustomerGreetPanel(QFrame) : 
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.parent_stackedWidgets = parent_stackedWidgets
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(0,0,0,50)
        dineInBtn = QDineInButton()
        takeOutBtn = QTakeOutButton()
        self.setObjectName("Greet")
        self.setStyleSheet("#Greet {background-color:#C8161D; }")


        dineInBtn.clicked.connect(lambda: self.handleChoice_clicked("dine_in"))
        takeOutBtn.clicked.connect(lambda: self.handleChoice_clicked("take_out"))

        btns_Hbox = QHBoxLayout()
        btns_Hbox.setSpacing(50)
        
        btns_Hbox.addStretch()
        btns_Hbox.addWidget(dineInBtn)
        btns_Hbox.addWidget(takeOutBtn)
        btns_Hbox.addStretch()

        greetMsg = QLabel("Where will you be eating today?")
        greetMsg.setFont(QFont("Helvetica", 30, QFont.Weight.Bold))
        greetMsg.setStyleSheet("background: transparent;color:white;")
        greetMsg.setFixedHeight(50)

        main_layout.addStretch()
        main_layout.addWidget(QLogoButton("assets/icons/pfp_icon.svg", "M'sKitchen", None), alignment=Qt.AlignmentFlag.AlignCenter )
        main_layout.addWidget(greetMsg, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(btns_Hbox)
        main_layout.addStretch()
        
            # dine in takeout options

    def handleChoice_clicked(self, choice) :
        self.parent_stackedWidgets.setCurrentIndex(0)
        pubsub.publish("choice_clicked", choice)


class QCustomerConfirmOrderPanel(QFrame) : 
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.parent_stackedWidgets = parent_stackedWidgets

        self.main_layout = QVBoxLayout(self)

        self.buttons_layout = QHBoxLayout()
        self.confirmBtn = QPushButton("confirm")
        self.cancelBtn = QPushButton("cancel")
        self.confirmBtn.clicked.connect(self.handleConfirm_clicked)
        self.cancelBtn.clicked.connect(self.handleCancel_clicked)
        self.buttons_layout.addWidget(self.confirmBtn)
        self.buttons_layout.addWidget(self.cancelBtn)

        self.contents_layout = QVBoxLayout() 

        self.main_layout.addLayout(self.contents_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.cartItemsArr = None
        pubsub.subscribe("submitOrder_clicked", self.handleSubmitOrder_clicked)
    
    def handleSubmitOrder_clicked(self, submitParams) :
        self.cartItemsArr, self.submitorder_callback, self.choice = submitParams
        self.parent_stackedWidgets.setCurrentIndex(2) 
        self.setContent()        

    def setContent(self) :
        self.contents_layout.addWidget(QLabel(f"confirm order - {self.choice} "))
        for item in self.cartItemsArr :
            self.contents_layout.addWidget(QLabel(f"{item.foodname} {item.getQuantity()}"))

        # confirm order, set contents function
    def handleCancel_clicked(self) :
        self.clear_layout(self.contents_layout)
        self.parent_stackedWidgets.setCurrentIndex(0)
    
    def handleConfirm_clicked(self) :
        self.submitorder_callback()
        self.parent_stackedWidgets.setCurrentIndex(3)
        # in print panel, just fetch the latest order...
        self.clear_layout(self.contents_layout)

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)  


class QCustomerPrintingPanel(QFrame) :
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.parent_stackedWidgets = parent_stackedWidgets
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(QLabel("Your receipt for your order is currently printing, please wait!"))
        newOrderBtn = QPushButton("new order")
        self.main_layout.addWidget(newOrderBtn)
        newOrderBtn.clicked.connect(self.handleNewOrder_clicked)

    def handleNewOrder_clicked(self) :
        self.parent_stackedWidgets.setCurrentIndex(1)

