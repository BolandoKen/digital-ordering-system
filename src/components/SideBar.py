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
from src.components.ScrollArea import QScrollAreaLayout
import traceback

class QSideBar(QFrame) :
    def __init__(self, pageName, switchPage = None) :
        super().__init__()
        self.pageName = pageName
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: white; color: black")
        self.cartItems = []
        self.cartItems_amount = []
        self.scroll_layout = QVBoxLayout(self)


        if self.pageName == "admin" :
            self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout)

            self.switchPage = switchPage
            self.logoutBtn = QPushButton("Log out")
            self.scroll_layout.addWidget(self.logoutBtn)
            self.init_adminSideBar()
        elif self.pageName == "customer" :
            title = QLabel("Your Cart")
            self.scroll_layout.addWidget(title)
            title.setStyleSheet("""
                    font-size: 16px;
                    font-weight: bold;
                    padding-bottom: 10px;
                    qproperty-alignment: AlignCenter;
                """)
            self.sidebar_layout = QScrollAreaLayout(QVBoxLayout, self.scroll_layout)
            self.submitBtn = QPushButton("SubmitBtn")
            self.scroll_layout.addWidget(self.submitBtn)
            self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
            pubsub.subscribe("addToCart", self.handleFoodAddToCart)
            self.init_customerSideBar()


    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout.getLayout())
        self.renderCartItems()
        self.sidebar_layout.addStretch()

        self.submitBtn.setEnabled(len(self.cartItems) > 0)
    
    def init_adminSideBar(self) :
        print('adminSidebar')
        self.switchBtn = QPushButton("switch admin panel")
        self.switchBtn.clicked.connect(self.switchPage)
        self.sidebar_layout.addWidget(self.switchBtn)
        self.logoutBtn.clicked.connect(self.handleLogoutClicked)
        self.sidebar_layout.addStretch()

    
    def handleLogoutClicked(self) :
        pubsub.publish("logout_Event", None)

    def handleSubmitOrderClicked(self) :
        if not self.cartItems:
            print("Cart is empty")
            return []

        item_counts = {}
        for i in range(0, self.sidebar_layout.getLayout().count()):
            item = self.sidebar_layout.getLayout().itemAt(i)
            if item and (widget := item.widget()) and isinstance(widget, QSimpleCartItem):
                food_id = widget.foodid 
                quantity = widget.getQuantity()
                if food_id in item_counts:
                    item_counts[food_id] += quantity
                if food_id in item_counts:
                    item_counts[food_id] += quantity
                else:
                    item_counts[food_id] = quantity

        self.cartItems = []
        self.init_customerSideBar()
        orderitem_info = [(quantity,food_id) for food_id, quantity in item_counts.items()] #should return a list of tuples based on whats inside the dict

        print(orderitem_info)

        confirmation = True # placeholder for confirmation dialog
        if confirmation :
            addOrder(orderitem_info)

    def handleFoodAddToCart(self, foodTuple) :
        fooditem_id, foodname = foodTuple
        if any(item[0] == fooditem_id for item in self.cartItems):
            print(fooditem_id,foodname," is a duplicate")
            return
        self.cartItems.append((fooditem_id, foodname))
        self.init_customerSideBar()
        print(fooditem_id,foodname, " added to cart")
    
    def renderCartItems(self) :
        if not self.cartItems :
            return
        for foodid, foodname in self.cartItems :
            self.sidebar_layout.addWidget(QSimpleCartItem(foodid, foodname, "icecream.png")) 

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    
class QSimpleCartItem(QFrame) : # refactor this later
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