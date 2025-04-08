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
    QSpinBox
)
from src.utils.PubSub import pubsub
from src.database.Orders import addOrder
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import traceback

class QSideBar(QFrame) :
    def __init__(self, pageName, switchPage = None) :
        super().__init__()
        self.pageName = pageName
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: white; color: black")
        self.cartItems = []
        self.cartItems_amount = []
        self.sidebar_layout = QVBoxLayout(self)
        if self.pageName == "admin" :
            self.switchPage = switchPage
            self.init_adminSideBar()
        elif self.pageName == "customer" :
            self.init_customerSideBar()
            pubsub.subscribe("addToCart", self.handleFoodAddToCart)


    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout)
        title = QLabel("Your Cart")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding-bottom: 10px;
            qproperty-alignment: AlignCenter;
        """)
        self.sidebar_layout.addWidget(title)
        self.renderCartItems()
        self.sidebar_layout.addStretch()
        self.submitBtn = QPushButton("SubmitBtn")
        self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
        self.sidebar_layout.addWidget(self.submitBtn)
        self.submitBtn.setEnabled(len(self.cartItems) > 0)
    
    def init_adminSideBar(self) :
        print('adminSidebar')
        self.switchBtn = QPushButton("switch admin panel")
        self.switchBtn.clicked.connect(self.switchPage)
        self.sidebar_layout.addWidget(self.switchBtn)
    
    def handleSubmitOrderClicked(self) :
        if not self.cartItems:
            print("Cart is empty")
            return
    
       # need to refactor this......
        item_counts = {}    #gave up and used chatgpt cuz always 1 quantity ra mu print sa akoa code huhu (1 shrimp, 1 squid balag 3 shrimp, 2 squid sa Spinbox)
        for i in range(1, self.sidebar_layout.count()):
            item = self.sidebar_layout.itemAt(i)
            if item and (widget := item.widget()) and isinstance(widget, QSimpleCartItem):
                foodname = widget.foodname
                quantity = widget.getQuantity()
                if foodname in item_counts:
                    item_counts[foodname] += quantity
                else:
                    item_counts[foodname] = quantity      
        receipt_lines = [(count, name) for name, count in item_counts.items()]
        #
        print(receipt_lines)
        # addOrder(receipt_lines)
        self.cartItems = [] #reset the cart
        self.init_customerSideBar()

    def handleFoodAddToCart(self, foodTuple) :
        # traceback.print_stack()
        fooditem_id, foodname = foodTuple
        if any(item[0] == fooditem_id for item in self.cartItems):
            print(fooditem_id,foodname," is a duplicate")
            return
        self.cartItems.append((fooditem_id, foodname))
        self.init_customerSideBar()
        # handle when same fooditem is clicked twice, instead of cartItems as arr maybe make it a dict 
        print(fooditem_id,foodname, " added to cart")
    
    def renderCartItems(self) :
        if not self.cartItems :
            return
        for foodid, foodname in self.cartItems :
            self.sidebar_layout.addWidget(QSimpleCartItem(foodid, foodname, "icecream.png")) # instead of a qlabe

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    
class QSimpleCartItem(QFrame) :
    def __init__(self, foodid, foodname, imgfile):
        super().__init__()
        self.setStyleSheet("background-color: white; color: black")
        self.foodid = foodid
        self.foodname = foodname
        self.cartItem_layout = QVBoxLayout(self)

        self.img_label = QLabel()
        pixmap = QPixmap(f"assets/foodimg/{imgfile}")
        self.img_label.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cartItem_layout.addWidget(self.img_label)

        self.quantityBox = QSpinBox()
        self.quantityBox.setValue(1)
        self.cartItem_layout.addWidget(QLabel(foodname))
        self.cartItem_layout.addWidget(self.quantityBox)

    def getQuantity(self):
        return self.quantityBox.value()