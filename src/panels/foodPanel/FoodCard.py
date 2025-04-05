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
    QLineEdit
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class QFoodItemCard(QFrame) : # at the mean time make it a QPushBtn for simplicity
    # card for each food item, display name, img, price
    def __init__(self, text, pageName) : 
        super().__init__()
        self.pageName = pageName
        self.foodCard_layout = QVBoxLayout(self)
        self.text = text
        self.foodLabel = QLabel(self.text)
        self.foodimg = QLabel()

        path = os.path.join(os.path.abspath("assets/foodimg"), "icecream.jpg") # pls do refactor later
        pixmap = QPixmap(path)
        self.foodimg.setPixmap(pixmap)
        self.foodimg.setFixedSize(100,100)
        self.foodimg.setScaledContents(True)
        self.setStyleSheet("background-color: white; color: black")
        
        if self.pageName == "admin" :
            self.init_adminFoodItemCard()
        elif self.pageName == "customer" :
            self.init_customerFoodItemCard()
        self.foodCard_layout.addWidget(self.foodLabel)   
        self.foodCard_layout.addWidget(self.foodimg) 

    def init_customerFoodItemCard(self) :
        self.foodLabel.setText(self.text) # do nothing
        # no edit/del btns

    def init_adminFoodItemCard(self) :
        self.foodLabel.setText(self.text + "  edit/del btns")
        # has edit/del btns , edit/trash icons in the card
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.addToCart()

    def addToCart(self) :
        print(f"add to order cart {self.text}")
