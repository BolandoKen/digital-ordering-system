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
import traceback

class QSideBar(QFrame) :
    def __init__(self, pageName, switchPage = None) :
        super().__init__()
        self.pageName = pageName
        self.setFixedWidth(300)
        self.cartItems = []
        self.cartItems_amount = []
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(0,0,0,10)
        self.scroll_layout.setSpacing(0)
        self.setStyleSheet("background-color: white; color: black;border-left: 1px solid #d9d9d9")

        if self.pageName == "admin" :
            self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")

            self.switchPage = switchPage
            self.logoutBtn = QPrimaryButton("Log out", 90, 30, 20)
            self.scroll_layout.addWidget(self.logoutBtn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.init_adminSideBar()
        elif self.pageName == "customer" :
            title = QLabel("My Orders")
            self.scroll_layout.addWidget(title)
            title.setFont(QFont("Helvetica", 15, QFont.Weight.Bold))
            title.setStyleSheet("""
                    qproperty-alignment: AlignCenter;
                """)
            self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout, "sidebar")
            self.total_label = QLabel("Total: ₱0.00")
            self.total_label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
            self.scroll_layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignCenter)

            self.submitBtn = QPrimaryButton("Done", 70, 30, 20)
            self.scroll_layout.addWidget(self.submitBtn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
            pubsub.subscribe("addToCart", self.handleFoodAddToCart)
            self.init_customerSideBar()

    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout.getLayout())
        self.renderCartItems()
        self.sidebar_layout.addStretch()
        self.submitBtn.setEnabled(len(self.cartItems) > 0)
    
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

    def handleSubmitOrderClicked(self) :
        if not self.cartItems:
            print("Cart is empty")
            return []
      
        valid_items = [(fid, fname, qty, imgfile, price) for fid, fname, qty, imgfile, price in self.cartItems if qty > 0] #chatgpt lessened my code to this bruh
        orderitem_info = [(qty, fid) for fid, fname, qty, imgfile, price in valid_items]

        confirmation = True # placeholder for confirmation dialog
        if confirmation :
            addOrder(orderitem_info)
            pubsub.publish("orderSubmitted_event")
            self.cartItems = []
            self.init_customerSideBar()

    def handleFoodAddToCart(self, foodTuple) :
        fooditem_id, foodname, imgfile, price = foodTuple
        for item in self.cartItems:
            if item[0] == fooditem_id:
                print(f"{foodname} already in cart")
                return
        self.cartItems.append((fooditem_id, foodname, 1, imgfile, price))
        self.init_customerSideBar()
        print(fooditem_id,foodname,price, " added to cart")
    
    def renderCartItems(self) :
        if not self.cartItems:
            self.total_label.setText("Total: ₱0.00") 
            return
            
        total = 0
        for f_item in self.cartItems:
            foodid, foodname, item_quantity, imgfile, price = f_item
            f_item_widget = QSimpleCartItem(foodid, foodname, imgfile, price)
            f_item_widget.quantityBox.setValue(item_quantity)
            f_item_widget.quantityBox.valueChanged.connect(
                lambda val, fid=foodid: self.handleQuantityChanged(fid, val)
            )
            self.sidebar_layout.addWidget(f_item_widget)
            total += f_item_widget.getSubtotal()
            
        self.total_label.setText(f"Total: ₱{total:.2f}")

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
    def __init__(self, foodid, foodname, imgfile, price):
        super().__init__()
        self.setStyleSheet("background-color: white; color: black")
        self.foodid = foodid
        self.foodname = foodname
        self.price = price
        self.cartItem_layout = QVBoxLayout(self)

        self.img_label = QLabel()
        # pixmap = QPixmap(f"assets/foodimg/{imgfile}")
        pixmap = imgfile
        self.img_label.setPixmap(pixmap)
        self.img_label.setFixedSize(100,100)
        self.img_label.setScaledContents(True)
        self.cartItem_layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignCenter)


        name_price_layout = QHBoxLayout()
        name_price_layout.addWidget(QLabel(foodname))
        self.price_label = QLabel(f"₱{price:.2f}")
        name_price_layout.addWidget(self.price_label)
        self.cartItem_layout.addLayout(name_price_layout)

        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Quantity:"))
        
        self.quantityBox = QSpinBox()
        self.quantityBox.setValue(1)
        self.cartItem_layout.addWidget(self.quantityBox)
        quantity_layout.addWidget(self.quantityBox)

        self.cartItem_layout.addLayout(quantity_layout)
        self.subtotal_label = QLabel(f"Subtotal: ₱{price:.2f}")
        self.cartItem_layout.addWidget(self.subtotal_label)

        self.quantityBox.valueChanged.connect(self.update_subtotal)

    def getQuantity(self):
        return self.quantityBox.value()
    
    def update_subtotal(self):
        subtotal = self.price * self.quantityBox.value()
        self.subtotal_label.setText(f"Subtotal: ₱{subtotal:.2f}")
        return subtotal
    
    def getSubtotal(self):
        return self.price * self.quantityBox.value()


