import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QSpinBox,
    QHBoxLayout,
    QSpacerItem
)
from src.utils.PubSub import pubsub
from src.database.Orders import addOrder
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from src.components.ScrollArea import QScrollAreaLayout
from src.components.Buttons import QPrimaryButton
from src.components.SpinBox import QCartItemSpinBox
import traceback

class QSideBar(QFrame) :
    def __init__(self) :
        super().__init__()
        self.setFixedWidth(250)
        self.cartItems = []
        self.cartItems_amount = []
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(0,0,0,10)
        self.scroll_layout.setSpacing(0)
        self.setStyleSheet("background-color: white; color: black;border-left: 1px solid #d9d9d9")



class QAdminSideBar(QSideBar) : 
    def __init__(self, switchPage=None):
        super().__init__()
        self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")

        self.switchPage = switchPage
        self.logoutBtn = QPrimaryButton("Log out", 90, 30, 20)
        self.scroll_layout.addWidget(self.logoutBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.init_adminSideBar()

    def init_adminSideBar(self) :
        self.currindex = 0 
        pubsub.subscribe("backToFoodPanel_clicked", self.handlePanelBtnClicked)
        self.AccPanelBtn = QPushButton("Account")
        self.StatsPanelBtn = QPushButton("Statistics")
        self.AccPanelBtn.clicked.connect(lambda: self.handlePanelBtnClicked(2))
        self.StatsPanelBtn.clicked.connect(lambda: self.handlePanelBtnClicked(1))
        self.sidebar_layout.addItem(QSpacerItem(50,150))
        self.sidebar_layout.addWidget(self.AccPanelBtn)
        self.sidebar_layout.addWidget(self.StatsPanelBtn)
        self.logoutBtn.clicked.connect(self.handleLogoutClicked)
        self.sidebar_layout.addStretch()

    def handlePanelBtnClicked(self, index) :
        self.StatsPanelBtn.setStyleSheet("background-color: white; color: black;")
        self.AccPanelBtn.setStyleSheet("background-color: white; color: black")
        if index == 1 : 
            self.StatsPanelBtn.setStyleSheet("background-color: #a1a1a1; color: black")
        elif index == 2 :
            self.AccPanelBtn.setStyleSheet("background-color: #a1a1a1; color: black")
        self.switchPage(index)
    
    def handleLogoutClicked(self) :
        pubsub.publish("logout_Event", None)

class QCustomerSideBar(QSideBar) :
    def __init__(self) :
        super().__init__()
        # self.scroll_layout.addItem(QSpacerItem(50,100))
        title = QLabel("My Orders")
        self.scroll_layout.addWidget(title)
        title.setFont(QFont("Helvetica", 15, QFont.Weight.Bold))
        title.setStyleSheet("""
                qproperty-alignment: AlignCenter;
                margin-top: 110px;
                border-bottom: 1px solid #d9d9d9;
                padding-bottom: 20px;
            """)
        self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")
        self.sidebar_layout.getLayout().setContentsMargins(0,0,0,0)
        self.sidebar_layout.getLayout().setSpacing(0)
        self.sidebar_layout.getLayout().setAlignment(Qt.AlignmentFlag.AlignTop)


        self.totalContainer = QFrame()
        self.totalContainer.setStyleSheet("border-top: 1px solid #d9d9d9;padding-top: 30px")
        self.totalContainer_Vbox = QVBoxLayout(self.totalContainer)
        self.totalContainer_Vbox.setContentsMargins(0,0,0,0)
        self.totalContainer_Vbox.setSpacing(5)
        self.totalText_label = QLabel("Total") 
        self.totalText_label.setStyleSheet("border:none;margin:0px;padding:0px;color: #a1a1a1;")
        self.total_label = QLabel("₱0.00")
        self.total_label.setFont(QFont("Helvetica", 15, QFont.Weight.Bold))
        self.total_label.setStyleSheet("border:none;margin-bottom: 0px;padding:0px;")

        self.submitBtn = QPrimaryButton("Done", 70, 30, 20)
        self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
    
        self.totalContainer_Vbox.addWidget(self.totalText_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totalContainer_Vbox.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totalContainer_Vbox.addWidget(self.submitBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.totalContainer)


        pubsub.subscribe("addToCart", self.handleFoodAddToCart)
        self.total = 0 
        self.init_customerSideBar()

    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout.getLayout())
        self.cartItems = []
        self.total = 0
        self.recalculate_total()
        # self.renderCartItems()
        # self.sidebar_layout.addStretch()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)
    
    def handleSubmitOrderClicked(self) :
        if not self.cartItems:
            print("Cart is empty")
            return []
      
        # valid_items = [(fid, fname, qty, imgfile, price) for fid, fname, qty, imgfile, price in self.cartItems if qty > 0] #chatgpt lessened my code to this bruh
        # orderitem_info = [(qty, fid) for fid, fname, qty, imgfile, price in valid_items]
        orderitem_info = []
        for item in self.cartItems :
            orderitem_info.append((item.getQuantity(), item.foodid))
        

        confirmation = True # placeholder for confirmation dialog
        if confirmation :
            addOrder(orderitem_info)
            pubsub.publish("orderSubmitted_event")
            self.init_customerSideBar()

    def handleFoodAddToCart(self, foodTuple) :
        fooditem_id, foodname, imgfile, price = foodTuple

        for item in self.cartItems :
            if item.foodid == fooditem_id :
                print(f"{foodname} already in cart")
                return
        new_cartItem = QSimpleCartItem(fooditem_id, foodname, imgfile, price, self.recalculate_total)
        new_cartItem.closeButton.clicked.connect(lambda _, foodid= fooditem_id: self.removeItemFromCart(foodid))
        self.cartItems.append(new_cartItem)
        # for item in self.cartItems:
        #     if item[0] == fooditem_id:
        #         print(f"{foodname} already in cart")
        #         return
        # self.cartItems.append((fooditem_id, foodname, quantity, imgfile, price))
        # self.init_customerSideBar() 
        self.sidebar_layout.addWidget(new_cartItem)
        self.recalculate_total()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)

        print(fooditem_id,foodname,price, " added to cart")
    
    def removeItemFromCart(self, foodid) :
        print(foodid)
        newCartItem = []
        widgetToRemove = None
        for item in self.cartItems :
            if item.foodid == foodid :
                widgetToRemove = item
                continue
            newCartItem.append(item)
        self.cartItems = newCartItem 
        self.sidebar_layout.getLayout().removeWidget(widgetToRemove)
        widgetToRemove.deleteLater()
        self.recalculate_total()
    
    def recalculate_total(self, e =None) :
        if not self.cartItems:
            self.total_label.setText("₱0.00") 
            return
        total = 0
        for item in self.cartItems :
            total += item.getSubtotal()
        self.total_label.setText(f"₱{total:.2f}")
        self.total = total

    def renderCartItems(self) :
        if not self.cartItems:
            self.total_label.setText("₱0.00") 
            return
            
        total = 0

        for item in self.cartItems :
            self.sidebar_layout.addWidget(item)
            total += item.getSubTotal()
        
        self.total_label.setText(f"Total: ₱{total:.2f}")
        # total = 0
        # for f_item in self.cartItems:
        #     foodid, foodname, item_quantity, imgfile, price = f_item
        #     f_item_widget = QSimpleCartItem(foodid, foodname, imgfile, price)
        #     f_item_widget.quantityBox.setValue(item_quantity)
        #     f_item_widget.quantityBox.valueChanged.connect(
        #         lambda val, fid=foodid: self.handleQuantityChanged(fid, val)
        #     )
        #     self.sidebar_layout.addWidget(f_item_widget)
        #     total += f_item_widget.getSubtotal()
            
        # self.total_label.setText(f"Total: ₱{total:.2f}")

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    
    def handleQuantityChanged(self, food_id, new_quantity):
        updated_cart = []
        for item in self.cartItems:
            fid, fname, qty, imgfile, price = item
            if fid == food_id:
                updated_cart.append((fid, fname, new_quantity, imgfile, price))
            else:
                updated_cart.append(item)
        self.cartItems = updated_cart
        self.init_customerSideBar()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)

class QSimpleCartItem(QFrame) : # refactor this later
    def __init__(self, foodid, foodname, imgfile, price, recalculate_cb):
        super().__init__()
        self.recalculate_cb = recalculate_cb
        self.setStyleSheet("""
                           #cartItem {
                            border-bottom: 1px solid #D9D9D9;
                           padding: 5px;
                           }
                           #cartItem > *{background-color: white; color: black; border: none;}""")
        self.setObjectName("cartItem") 
        self.foodid = foodid
        self.foodname = foodname
        self.price = price
        self.cartItem_layout = QVBoxLayout(self)
        self.cartItem_layout.setContentsMargins(0,0,0,0)
        self.cartItem_layout.setSpacing(0)
        self.cartItem_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.img_label = QLabel()
        # pixmap = QPixmap(f"assets/foodimg/{imgfile}")
        pixmap = imgfile
        self.img_label.setPixmap(pixmap)
        self.img_label.setFixedSize(100,100)
        self.img_label.setScaledContents(True)
        self.closeButton = QPushButton("x")
        self.closeButton.setFixedWidth(50)
        self.closeButton.setCursor(Qt.CursorShape.PointingHandCursor)

        # self.setFixedWidth(50)
        self.price_close_hbox = QHBoxLayout()
        self.subtotal_label = QLabel(f"₱{price:.2f}")
        self.subtotal_label.setStyleSheet("margin: 10px")
        self.price_close_hbox.addWidget(self.subtotal_label)
        self.price_close_hbox.addStretch()
        self.price_close_hbox.addWidget(self.closeButton)


        self.cartItem_layout.addLayout(self.price_close_hbox)
        self.cartItem_layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignCenter)

        
        self.quantityBox = QSpinBox()
        self.quantityBox.setValue(1)

        self.cartItem_layout.addWidget(QLabel(foodname), alignment=Qt.AlignmentFlag.AlignCenter)
        self.cartItem_layout.addWidget(QLabel(f"₱{str(price)}"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.customQuanBox = QCartItemSpinBox()
        self.cartItem_layout.addWidget(self.customQuanBox, alignment=Qt.AlignmentFlag.AlignCenter)
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


