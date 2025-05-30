from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QHBoxLayout,
    QSpacerItem,
)
from src.utils.PubSub import pubsub
from src.database.Orders import addOrder
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import  QFont
from src.components.ScrollArea import QScrollAreaLayout
from src.components.Buttons import QPrimaryButton, QDeleteButton, QAdminButton, QCloseButton
from src.components.SpinBox import QCartItemSpinBox
from src.components.Dialogs import QConfirmDialog

class QSideBar(QFrame) :
    def __init__(self) :
        super().__init__()
        self.setFixedWidth(300)
        self.cartItems = []
        self.cartItems_amount = []
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(0,0,0,10)
        self.scroll_layout.setSpacing(0)
        self.setStyleSheet("background-color: white; color: black;border-left: 2px solid #CFCFCF")

class QAdminSideBar(QSideBar) : 
    def __init__(self, switchPage=None):
        super().__init__()
        self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")

        self.switchPage = switchPage
        self.logoutBtn = QPrimaryButton("Log out", 180, 60, 30,)
        self.scroll_layout.addWidget(self.logoutBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addItem(QSpacerItem(20, 40))
        self.init_adminSideBar()

    def init_adminSideBar(self) :
        self.currindex = 0 
        pubsub.subscribe("backToFoodPanel_clicked", self.handlePanelBtnClicked)
        self.AccPanelBtn = QAdminButton("Profile", "border-bottom: none;")
        self.StatsPanelBtn = QAdminButton("Statistics", )
        self.AccPanelBtn.clicked.connect(lambda: self.handlePanelBtnClicked(2))
        self.StatsPanelBtn.clicked.connect(lambda: self.handlePanelBtnClicked(1))
        self.sidebar_layout.addItem(QSpacerItem(50,150))
        self.sidebar_layout.addWidget(self.AccPanelBtn)
        self.sidebar_layout.addWidget(self.StatsPanelBtn)
        self.logoutBtn.clicked.connect(self.handleLogoutClicked)
        self.sidebar_layout.addStretch()
        pubsub.subscribe("logout_Event", self.setCurrIndexToZero)

    def handlePanelBtnClicked(self, index) :
        if self.currindex == index :
            return
        pubsub.publish("adminPanelSwitched")
        self.AccPanelBtn.setClickedState(False)
        self.StatsPanelBtn.setClickedState(False)
        if index == 1 : 
            self.StatsPanelBtn.setClickedState(True)
        elif index == 2 :
            self.AccPanelBtn.setClickedState(True)
        self.currindex = index
        self.switchPage(index)
    
    def setCurrIndexToZero(self, e= None) :
        self.currindex = 0 
        self.AccPanelBtn.setClickedState(False)
        self.StatsPanelBtn.setClickedState(False)

    def handleLogoutClicked(self) :
        dialog = QConfirmDialog("Log Out", "Are you sure you want to log out?", self)
        if dialog.exec():
            self.AccPanelBtn.setClickedState(False)
            self.StatsPanelBtn.setClickedState(False)
            pubsub.publish("logout_Event", None)

            
class QCustomerSideBar(QSideBar) :
    def __init__(self) :
        super().__init__()
        title = QLabel("My\nOrders")
        self.scroll_layout.addWidget(title)
        title.setFont(QFont("Helvetica", 40, QFont.Weight.Bold))
        title.setStyleSheet("""
                qproperty-alignment: AlignLeft;
                margin-top: 110px;
                border-bottom: 2px solid #CFCFCF;
                padding-bottom: 20px;

            """)
        self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")
        self.sidebar_layout.getLayout().setContentsMargins(0,0,0,0)
        self.sidebar_layout.getLayout().setSpacing(0)
        self.sidebar_layout.getLayout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.choice = None
        pubsub.subscribe("choice_clicked", self.setChoice)

        self.totalContainer = QFrame()
        self.totalContainer.setStyleSheet("border-top: 2px solid #d9d9d9;padding-top: 30px")
        self.totalContainer_Vbox = QVBoxLayout(self.totalContainer)
        self.totalContainer_Vbox.setContentsMargins(0,0,0,0)
        self.totalContainer_Vbox.setSpacing(5)
        self.totalText_label = QLabel("Total") 
        self.totalText_label.setFont(QFont("Helvetica", 20))
        self.totalText_label.setStyleSheet("border:none;margin:0px;padding:0px;color: #A1A1A1;")
        self.total_label = QLabel("₱0.00")
        self.total_label.setFont(QFont("Helvetica", 40, QFont.Weight.Bold))
        self.total_label.setStyleSheet("border:none;margin-bottom: 0px;padding:0px;")

        self.submitBtn = QPrimaryButton("Done", 180, 60, 30)
        self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
    
        self.totalContainer_Vbox.addWidget(self.totalText_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totalContainer_Vbox.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totalContainer_Vbox.addWidget(self.submitBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totalContainer_Vbox.addItem(QSpacerItem(20, 40))
        self.scroll_layout.addWidget(self.totalContainer)


        pubsub.subscribe("addToCart", self.handleFoodAddToCart)
        self.total = 0 
        self.init_customerSideBar()

    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout.getLayout())
        self.cartItems = []
        self.total = 0
        self.recalculate_total()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)
    
    def setChoice(self, choice) :
        self.choice = choice

    def handleSubmitOrderClicked(self) :
        if not self.cartItems:
            print("Cart is empty")
            return []
      
        orderitem_info = []
        for item in self.cartItems :
            orderitem_info.append((item.getQuantity(), item.foodid))
        
        pubsub.publish("submitOrder_clicked", (self.cartItems, self.submitCheckoutCallback, self.choice, self.sidebar_layout)) # should also probably pass cb

    def submitCheckoutCallback(self) :
        orderitem_info = []
        for item in self.cartItems :
            orderitem_info.append((item.getQuantity(), item.foodid))
        
        addOrder(orderitem_info)
        pubsub.publish("orderSubmitted_event")
        self.init_customerSideBar()

        return True

    def handleFoodAddToCart(self, foodTuple) :
        fooditem_id, foodname, imgfile, price = foodTuple

        for item in self.cartItems :
            if item.foodid == fooditem_id :
                print(f"{foodname} already in cart")
                return
        new_cartItem = QSimpleCartItem(fooditem_id, foodname, imgfile, price, self.recalculate_total)
        new_cartItem.closeBtn_cartState.clicked.connect(lambda _, foodid= fooditem_id: self.removeItemFromCart(foodid))
        new_cartItem.closeBtn_confirmState.clicked.connect(lambda _, foodid= fooditem_id: self.removeItemFromCart(foodid))

        self.cartItems.append(new_cartItem)

        self.sidebar_layout.container.hide()
        self.sidebar_layout.addWidget(new_cartItem)
        self.sidebar_layout.container.show()

        self.recalculate_total()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)
        QTimer.singleShot(0, lambda: self.sidebar_layout.ensureWidgetVisible(new_cartItem))
        print(fooditem_id,foodname,price, " added to cart")
    
    def removeItemFromCart(self, foodid) :
        widget_remove = None
        for item in self.cartItems:
            if item.foodid == foodid:
                message = f"Are you sure you want to delete order {item.getQuantity()}x {item.foodname}?"
                dialog = QConfirmDialog("Confirm Delete", message, self.window())
                if not dialog.exec():
                    return 
                widget_remove = item
                break

        if widget_remove:
            self.cartItems.remove(widget_remove)
            self.sidebar_layout.getLayout().removeWidget(widget_remove)
            widget_remove.deleteLater()
            self.recalculate_total()
            pubsub.publish("cartItem_deleted", self.cartItems)
    
    def recalculate_total(self, e =None) :
        if not self.cartItems:
            self.total_label.setText("₱0.00") 
            pubsub.publish("recalculate_total", f"₱0.00" )
            return
        total = 0
        for item in self.cartItems :
            total += item.getSubtotal()
        self.total_label.setText(f"₱{total:.2f}")
        pubsub.publish("recalculate_total", f"₱{total:.2f}" )
        self.total = total

    def renderCartItems(self) :
        if not self.cartItems:
            self.total_label.setText("₱0.00") 
            return
            
        total = 0

        for item in self.cartItems :
            self.sidebar_layout.addWidget(item)
            total += item.getSubTotal()
        
        self.total_label.setText(f"₱{total:.2f}")


    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   

    def resetSidebar(self):
        self.clear_layout(self.sidebar_layout.getLayout())  # assuming you pass self.cartLayout
        self.cartItems.clear()
        self.totalAmount = 0
        self.total_label.setText("Total: ₱0.00")
        self.cart_state = "cart"
        self.submitBtn.setText("Done")

class QSimpleCartItem(QFrame) : # refactor this later
    def __init__(self, foodid, foodname, imgfile, price, recalculate_cb):
        super().__init__()
        self.recalculate_cb = recalculate_cb
        self.setStyleSheet("""
                           #cartItem {
                            border-bottom: 2px solid #D9D9D9;
                           padding: 5px;
                           }
                           #cartItem *{background-color: white; color: black; border: none;}""")
        self.setObjectName("cartItem") 
        self.foodid = foodid
        self.foodname = foodname
        self.price = price
        self.state = "cart"
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
    
        self.pixmap = imgfile 
        # # imgfile is reused pixmap passed by food card, should just setpixmapof since memoized, but im lazy to refactor
        
        self.closeBtn_cartState = QCloseButton()
        self.closeBtn_cartState.setFixedWidth(52)


        self.closeBtn_confirmState = QDeleteButton("confirm")
        self.closeBtn_confirmState.setFixedWidth(50)
        self.closeBtn_confirmState.setCursor(Qt.CursorShape.PointingHandCursor)

        self.subtotal_label = QLabel(f"₱{price:.2f}")
        self.subtotal_label.setStyleSheet("margin: 10px")

        self.foodname_label = QLabel(foodname)
        self.foodprice_label = QLabel(f"₱{str(price)}")
        self.foodprice_label.setStyleSheet("""
        font-size: 30px;
        font-weight: bold;
        color: #A1A1A1;
        qproperty-alignment: AlignCenter;
        """)
        self.customQuanBox = QCartItemSpinBox()

        self.itemDict_cart = {
            "subtotal_label" : self.subtotal_label,
            "closeBtn_cart" : self.closeBtn_cartState,
            "img_label_cart" : QLabel(),
            "foodname_label" : QLabel(foodname),
            "foodprice_label" : QLabel(f"₱{str(price)}"),
            "customQuanBox" : self.customQuanBox,
        }
        self.itemDict_confirm = {
            "closeBtn_confirm" : self.closeBtn_confirmState,
            "img_label_confirm" : QLabel(),
            "foodname_label" : QLabel(foodname),
            "foodprice_label" : QLabel(f"₱{str(price)}"),
            "customQuanBox" : self.customQuanBox,
        }
        

        self.itemDict_cart["img_label_cart"].setPixmap(self.pixmap)
        self.itemDict_cart["img_label_cart"].setFixedSize(100,100)
        self.itemDict_cart["img_label_cart"].setScaledContents(True)
        self.itemDict_cart["foodname_label"].setStyleSheet("font-family: Helvetica; font: 15px; color: #000000; font-weight: bold;")
        self.itemDict_cart["foodprice_label"].setStyleSheet("font-family: Helvetica; font: 20px; color: #A1A1A1; font-weight: bold;")

        self.itemDict_confirm["img_label_confirm"].setPixmap(self.pixmap)
        self.itemDict_confirm["img_label_confirm"].setFixedSize(100,100)
        self.itemDict_confirm["img_label_confirm"].setScaledContents(True)
        self.itemDict_confirm["foodname_label"].setStyleSheet("font-family: Helvetica; font: 30px; color: #FFFFFF; font-weight: bold;")
        self.itemDict_confirm["foodprice_label"].setStyleSheet("font-family: Helvetica; font: 20px; color: #FFFFFF; font-weight: regular;")


        self.cart_cartState_widget = QCart_cartState(self.itemDict_cart)
        self.cart_cartState_widget.addSpinBox()
        self.cart_confirmState_widget = QCart_confirmState(self.itemDict_confirm)
        self.cart_confirmState_widget.hide()

        self.main_layout.addWidget(self.cart_cartState_widget)
        self.main_layout.addWidget(self.cart_confirmState_widget)

        self.customQuanBox.connectOnChangeTo(self.update_subtotal)


    def getQuantity(self):
        return self.customQuanBox.getQuantity()
    
    def update_subtotal(self, e = None):
        subtotal = self.price * self.customQuanBox.getQuantity()
        self.subtotal_label.setText(f"₱{subtotal:.2f}")
        self.recalculate_cb()
        return subtotal
    
    def getSubtotal(self):
        return self.price * self.customQuanBox.getQuantity()

    def transitionState(self, e = None) :
        if self.state == "cart" :
            self.cart_cartState_widget.hide()
            self.cart_cartState_widget.removeSpinBox()
            self.cart_confirmState_widget.addSpinBox()
            self.cart_confirmState_widget.show()
            self.state = "confirm"
        elif self.state == "confirm" :
            self.cart_confirmState_widget.hide()
            self.cart_confirmState_widget.removeSpinBox()
            self.cart_cartState_widget.addSpinBox()
            self.cart_cartState_widget.show()
            self.state = "cart"
        self.customQuanBox.setState(self.state)


class QCart_cartState(QFrame) :
    def __init__(self, itemDict):
        super().__init__()
        self.itemDict = itemDict
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.subtotal_close_hbox = QHBoxLayout()
        self.subtotal_close_hbox.addWidget(self.itemDict["subtotal_label"])
        self.subtotal_close_hbox.addStretch()
        self.subtotal_close_hbox.addWidget(self.itemDict["closeBtn_cart"])

        self.placeholder_layout = QHBoxLayout()

        self.main_layout.addLayout(self.subtotal_close_hbox)
        self.main_layout.addWidget(self.itemDict["img_label_cart"], alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.itemDict["foodname_label"], alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.itemDict["foodprice_label"], alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.placeholder_layout)


    def addSpinBox(self) :
        self.placeholder_layout.addWidget(self.itemDict["customQuanBox"], alignment=Qt.AlignmentFlag.AlignCenter)
    
    def removeSpinBox(self) :
        self.placeholder_layout.removeWidget(self.itemDict["customQuanBox"])

class QCart_confirmState(QFrame) :
    def __init__(self, itemDict):
        super().__init__()
        self.itemDict = itemDict
        self.main_layout = QHBoxLayout(self) 
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet("background:transparent; color: white;")

        self.foodname_price_vbox = QVBoxLayout()
        self.foodname_price_vbox.addStretch()
        self.foodname_price_vbox.addWidget(self.itemDict["foodname_label"])
        self.foodname_price_vbox.addWidget(self.itemDict["foodprice_label"])
        self.foodname_price_vbox.addStretch()


        self.placeholder_layout = QHBoxLayout()
        self.placeholder_layout.setContentsMargins(0,0,0,0)

        self.main_layout.addWidget(self.itemDict["img_label_confirm"])
        self.main_layout.addLayout(self.foodname_price_vbox)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.placeholder_layout)
        self.main_layout.addWidget(self.itemDict["closeBtn_confirm"])

    def addSpinBox(self) :
        self.placeholder_layout.addWidget(self.itemDict["customQuanBox"], alignment=Qt.AlignmentFlag.AlignCenter)
    
    def removeSpinBox(self) :
        self.placeholder_layout.removeWidget(self.itemDict["customQuanBox"])