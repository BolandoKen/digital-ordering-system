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
    QLineEdit,
    QSpinBox
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class QFoodItemCard(QFrame) : # at the mean time make it a QPushBtn for simplicity
    # card for each food item, display name, img, price
    def __init__(self, foodTuple, pageName) : 
        super().__init__()
        self.pageName = pageName
        self.fooditem_id, self.foodname, self.price, self.imgfile = foodTuple
        self.foodCard_layout = QVBoxLayout(self)

        if self.pageName == "admin" :
            self.init_adminFoodItemCard()
        elif self.pageName == "customer" :
            self.init_customerFoodItemCard()
        elif self.pageName == "sideBar" :
            print('hmmm reuse?')

        self.setStyleSheet("background-color: white; color: black")

    def init_customerFoodItemCard(self) :
        self.foodLabel = QLabel(self.foodname)
        self.foodimg = QLabel()
        self.setPixMapOf(self.foodimg, self.imgfile)
        self.priceLabel = QLabel(str(self.price))        

        self.foodCard_layout.addWidget(self.foodLabel)   
        self.foodCard_layout.addWidget(self.foodimg) 
        self.foodCard_layout.addWidget(self.priceLabel)
        # no edit/del btns

    def init_adminFoodItemCard(self) :
        self.init_customerFoodItemCard()
        self.foodCard_layout.addWidget(QPushButton("edit"))
        self.foodCard_layout.addWidget(QPushButton("delete"))
        # has edit/del btns , edit/trash icons in the card

    def setPixMapOf(self, label, imgFileName) :
        if imgFileName is None :
            imgFileName = "icecream.png"
        path = os.path.join(os.path.abspath("assets/foodimg"), imgFileName) # pls do refactor later
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(50,50)
        label.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.handleAddToCart(self.fooditem_id, self.foodname)

    def handleAddToCart(self, fooditem_id, foodname) :
        # can do self.parent() now yay
        self.parent().parent().parent().parent().sideBar.handleFoodAddToCart(fooditem_id, foodname)
