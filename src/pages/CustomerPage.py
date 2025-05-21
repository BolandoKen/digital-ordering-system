from src.panels.foodPanel.FoodPanel import QFoodPanel
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QSpacerItem,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from src.components.SideBar import QCustomerSideBar
from src.components.Headers import QLogoHeader, QLogoButton
from src.components.Buttons import QDineInButton, QTakeOutButton, QTertiaryButton, QQuaternaryButton
from src.components.ScrollArea import QScrollAreaLayout
from src.utils.PubSub import pubsub
from src.database.queries import fetchLatest_orderid, fetchOrderItemsSubtotalList, fetchOrderItemsTotal, fetchOrderDateTime, ProfileQueries
from src.components.Dialogs import QConfirmDialog


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
        pubsub.subscribe("backBtn_clicked", self.customerPage_stackedWidgets.setCurrentIndex)
        
class QCustomerFoodMenuPanel(QFrame) :
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.objectName = "customer"
        self.foodPanel = QFoodPanel(self.objectName)
        self.sideBar = QCustomerSideBar()
        self.logoHeader = QLogoHeader("customer")
        self.customer_layout = QGridLayout(self)
        self.customer_layout.setSpacing(0)
        self.customer_layout.setContentsMargins(30,0,0,0)
        self.customer_layout.addWidget(self.logoHeader, 0,0)
        self.customer_layout.addWidget(self.foodPanel, 1, 0)
        self.customer_layout.addWidget(self.sideBar, 0, 1, 2, 1)

class QCustomerGreetPanel(QFrame) : 
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.parent_stackedWidgets = parent_stackedWidgets
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(0,0,0,50)
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

        self.main_layout.addStretch()
        self.main_layout.addWidget(QLogoButton("nocb"), alignment=Qt.AlignmentFlag.AlignCenter )
        self.main_layout.addWidget(greetMsg, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(btns_Hbox)
        self.main_layout.addStretch()
        
            # dine in takeout options

    def handleChoice_clicked(self, choice) :
        self.parent_stackedWidgets.setCurrentIndex(0)
        pubsub.publish("choice_clicked", choice)


class QCustomerConfirmOrderPanel(QFrame) : 
    def __init__(self, parent_stackedWidgets):
        super().__init__()
        self.setObjectName("Confirm")
        self.setStyleSheet("""
                           #Confirm {
                           background-color:#C8161D; 
                           }
                           #Confirm > * {
                           background: transparent;
                           color : white;
                           }
                           """)
        self.parent_stackedWidgets = parent_stackedWidgets

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30,0,35,35)
        self.main_layout.setSpacing(0)

        self.confirmBtn = QTertiaryButton("Checkout",300, 60, 35)
        self.cancelBtn = QQuaternaryButton("Back to Menu",300, 60, 35 )
        self.confirmBtn.clicked.connect(self.handleCheckout_clicked)
        self.cancelBtn.clicked.connect(self.handleCancel_clicked)
 

        self.choice_label = QLabel()
        self.choice_label.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))
        self.total_label = QLabel()
        self.total_label.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))


        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0,20,0,0)
        self.leftFoot_layout = QVBoxLayout()
        self.rightFoot_layout = QVBoxLayout()
        self.rightFoot_layout.setSpacing(20)

        self.footer_layout.addLayout(self.leftFoot_layout)
        self.footer_layout.addStretch()
        self.footer_layout.addLayout(self.rightFoot_layout)

        self.leftFoot_layout.setSpacing(0)
        self.leftFoot_layout.addSpacerItem(QSpacerItem(50,50))
        self.leftFoot_layout.addWidget(QLabel("Total : "), alignment=Qt.AlignmentFlag.AlignBottom)
        self.leftFoot_layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignBottom)

        self.rightFoot_layout.addWidget(self.confirmBtn)
        self.rightFoot_layout.addWidget(self.cancelBtn)

      
        self.main_layout.addWidget(QLogoHeader("confirmorder"))
        self.main_layout.addWidget(self.choice_label)
        self.scroll_arealayout = QScrollAreaLayout(QVBoxLayout, self.main_layout, "confirm")
        self.scroll_arealayout.getLayout().setContentsMargins(0,0,15,0)

        self.main_layout.addLayout(self.footer_layout)

        self.cartItemsArr = None
        self.printer_connected = False
        pubsub.subscribe("submitOrder_clicked", self.handleSubmitOrder_clicked)
        pubsub.subscribe("cartItem_deleted", self.updateCartItems)
        pubsub.subscribe("recalculate_total", self.update_totalText)
        pubsub.subscribe("printer_connected", self.setPrinterConnected)
    
    def setPrinterConnected(self, is_connected) :
        self.printer_connected = is_connected

    def handleSubmitOrder_clicked(self, submitParams) :
        self.cartItemsArr, self.submitcheckout_callback, self.choice, self.sidebar_layout = submitParams
        self.parent_stackedWidgets.setCurrentIndex(2) 

        self.setContent()        

    def setContent(self) :
        if self.choice == "dine_in" :
            self.choicestr = "Dine in"
        else :
            self.choicestr = "Take out"
        self.choice_label.setText(f"Confirm Order - {self.choicestr}")
        for item in self.cartItemsArr :
            self.sidebar_layout.getLayout().removeWidget(item)
            item.transitionState()
            self.scroll_arealayout.getLayout().addWidget(item, alignment = Qt.AlignmentFlag.AlignTop)
            self.scroll_arealayout.getLayout().setAlignment(Qt.AlignmentFlag.AlignTop)

        # confirm order, set contents function
    def handleCancel_clicked(self) :
        print(len(self.cartItemsArr))

        for item in self.cartItemsArr :
            self.scroll_arealayout.getLayout().removeWidget(item)
            item.transitionState()
            self.sidebar_layout.addWidget(item)

        self.parent_stackedWidgets.setCurrentIndex(0)
    
    def handleCheckout_clicked(self) :
        if not self.printer_connected :
            dialog = QConfirmDialog("Warning", "Printer not detected. Please connect a printer to continue.", self, single_button = True)
            dialog.exec()
            return 
        if not self.cartItemsArr :
            print("cart is empty")
            return
        #fetch latest orderId, #fetch orderitemssubtotal, total

        self.submitcheckout_callback() # add order cb
        self.parent_stackedWidgets.setCurrentIndex(3)

        profile_name = ProfileQueries.fetchProfileName()
        latest_orderid = fetchLatest_orderid()
        self.orderItemsSubtotalList = fetchOrderItemsSubtotalList(latest_orderid) 
        self.orderItemsTotal = fetchOrderItemsTotal(latest_orderid)
        order_datetime = fetchOrderDateTime(latest_orderid)
        myOrder = {
            "items" : self.orderItemsSubtotalList,
            "total" : self.orderItemsTotal,
            "orderid" : latest_orderid,
            "choice" : self.choicestr,
            "profile_name" : profile_name,
            "date" : order_datetime
        }
        pubsub.publish("orderConfirmed_event")
        pubsub.publish("print_event", myOrder)
        self.clear_layout(self.scroll_arealayout.getLayout())

    def updateCartItems(self, newCartItems) :
        self.cartItemsArr = newCartItems

    def update_totalText(self, totalText) :
        self.total_label.setText(totalText)

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
        self.setObjectName("Print")
        self.setStyleSheet("""
                           #Print {
                           background-color:#C8161D; 
                           }
                           #Print > * {
                           background: transparent;
                           color : white;
                           }
                           """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(40)
        
        self.msg_label = QLabel("Thank you! Your order has been placed!")
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setWordWrap(True)
        self.msg_label.setFixedSize(500,100)
        self.msg_label.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        self.msg2_label = QLabel('Your receipt is printing. Please hand it to the counter for food preparation.')
        self.msg2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg2_label.setWordWrap(True)
        self.msg2_label.setFixedSize(500,100)
        self.msg2_label.setFont(QFont("Helvitica", 15, QFont.Weight.Normal))

        self.orderno_label = QLabel()
        self.orderno_label.setStyleSheet("color: #FFCA40")
        self.orderno_label.setWordWrap(True)
        self.orderno_label.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        self.msg3_label = QLabel("Returning to Home in 5")
        self.msg3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg3_label.setWordWrap(True)
        self.msg3_label.setFixedSize(500,100)
        self.msg3_label.setFont(QFont("Helvitica", 15, QFont.Weight.Normal))

        msg3_sizepolicy = self.msg3_label.sizePolicy()
        msg3_sizepolicy.setRetainSizeWhenHidden(True)
        self.msg3_label.setSizePolicy(msg3_sizepolicy)

        self.newOrderBtn = QQuaternaryButton("Start New Order", 300, 60, 35)
        
        self.orderno_labellabel = QLabel("Order No:")
        self.orderno_labellabel.setFont(QFont("Helvitica", 25, QFont.Weight.Bold))

        orderno_vbox =QVBoxLayout()
        orderno_vbox.setContentsMargins(0,0,0,0)
        orderno_vbox.setSpacing(0)
        orderno_vbox.addWidget(self.orderno_labellabel, alignment=Qt.AlignmentFlag.AlignCenter)
        orderno_vbox.addWidget(self.orderno_label, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_timer_vbox = QVBoxLayout()
        btn_timer_vbox.setContentsMargins(0,0,0,0)
        btn_timer_vbox.setSpacing(0)
        btn_timer_vbox.addWidget(self.newOrderBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_timer_vbox.addWidget(self.msg3_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch()
        self.main_layout.addWidget(QLogoButton("nocb"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.msg_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.msg2_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(orderno_vbox)
        self.main_layout.addLayout(btn_timer_vbox)
       
        self.main_layout.addStretch()
        self.newOrderBtn.clicked.connect(self.handleNewOrder_clicked)
        self.newOrderBtn.setEnabled(False)
        self.msg3_label.hide()
        self.newOrderBtn.hide()
        pubsub.subscribe("orderConfirmed_event", self.setText_OrderId)
        pubsub.subscribe("print_finished", self.startTimer)

    def handleNewOrder_clicked(self) :
        self.parent_stackedWidgets.setCurrentIndex(1)
        self.mytimer.stop()
        self.mytimer.timeout.disconnect()

    
    def setText_OrderId(self, e = None) :
        self.orderno = str(fetchLatest_orderid())
        self.orderno_label.setText(self.orderno)
        self.msg3_label.hide()
        self.newOrderBtn.hide() # ??
    
    def startTimer(self, e=None) :
        self.newOrderBtn.setEnabled(True)
        self.msg3_label.show()
        self.newOrderBtn.show()
        self.mytimer = QTimer()
        self.mytimer.setSingleShot(True)
        self.mytimer.timeout.connect(lambda: self.timeRecurse) # init set up to disconnect in recursion

        # should only start after printing ends..
        self.timeRecurse(5)

    def timeRecurse(self, seconds) :
        self.msg3_label.setText(f"Returning to Home in {seconds}")
        if seconds == 0 :
            self.parent_stackedWidgets.setCurrentIndex(1)
            self.msg3_label.hide()
            self.newOrderBtn.hide()
            return
        seconds -= 1
        self.mytimer.start(1000)
        self.mytimer.timeout.disconnect()
        self.mytimer.timeout.connect(lambda:self.timeRecurse(seconds))

