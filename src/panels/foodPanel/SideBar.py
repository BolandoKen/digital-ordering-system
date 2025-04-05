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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class QSideBar(QFrame) :
    def __init__(self, pageName) :
        super().__init__()
        self.pageName = pageName
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: white; color: black")
        self.cartItems = []
        self.sidebar_layout = QVBoxLayout(self)
        if self.pageName == "admin" :
            self.init_adminSideBar()
        elif self.pageName == "customer" :
            self.init_customerSideBar()

    def init_customerSideBar(self) :
        self.clear_layout(self.sidebar_layout)
        self.renderCartItems()
        self.sidebar_layout.addStretch()
        self.submitBtn = QPushButton("SubmitBtn")
        self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
        self.sidebar_layout.addWidget(self.submitBtn)
    
    def init_adminSideBar(self) :
        print('adminSidebar')
    
    def handleSubmitOrderClicked(self) :
        print('will order, printing receipt')

    def handleFoodAddToCart(self, fooditem_id, foodname) :
        self.cartItems.append((fooditem_id, foodname))
        self.init_customerSideBar()
        # handle when same fooditem is clicked twice, instead of cartItems as arr maybe make it a dict 
        print(fooditem_id,foodname, "added to cart")
    
    def renderCartItems(self) :
        if not self.cartItems :
            return
        for foodid, foodname in self.cartItems :
            self.sidebar_layout.addWidget(QSimpleCartItem(foodid, foodname)) # instead of a qlabe

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    
class QSimpleCartItem(QFrame) :
    def __init__(self, foodid, foodname):
        super().__init__()
        self.foodid = foodid
        self.cartItem_layout = QVBoxLayout(self)
        self.quantityBox = QSpinBox()
        self.cartItem_layout.addWidget(QLabel(foodname))
        self.cartItem_layout.addWidget(self.quantityBox)
