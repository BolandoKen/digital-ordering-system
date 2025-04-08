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
from src.components.Dialogs import QeditDialog
from src.database.FoodItems import deleteFoodItem
from src.utils.PubSub import pubsub
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from src.utils.PixMap import setPixMapOf
from src.components.MenuCards import QMenuCard

class QFoodItemCard(QMenuCard) : 
    def __init__(self, foodTuple, pageName) : 
        super().__init__()
        self.pageName = pageName
        self.fooditem_id, self.foodname, self.price, self.imgfile, self.category_id = foodTuple
        self.editFoodDialog = QeditDialog("food", foodTuple)
        self.foodCard_layout = QVBoxLayout(self)

        if self.pageName == "admin" :
            self.init_adminFoodItemCard()
        elif self.pageName == "customer" :
            self.init_customerFoodItemCard()

        self.setStyleSheet("background-color: white; color: black")

    def init_customerFoodItemCard(self) :
        self.foodLabel = QLabel(self.foodname)
        self.foodimg = QLabel()
        setPixMapOf(self.foodimg, self.imgfile)
        self.priceLabel = QLabel(str(self.price))        

        self.foodCard_layout.addWidget(self.foodLabel)   
        self.foodCard_layout.addWidget(self.foodimg) 
        self.foodCard_layout.addWidget(self.priceLabel)
        # no edit/del btns

    def init_adminFoodItemCard(self) :
        self.init_customerFoodItemCard()
        self.delBtn = QPushButton("delete")
        self.delBtn.clicked.connect(self.handleFoodDel)
        self.foodCard_layout.addWidget(self.delBtn)
        # has edit/del btns , edit/trash icons in the card

    def handleFoodDel(self) :
        deleteFoodItem(self.fooditem_id)
        pubsub.publish("updateFoodItem")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.pageName == "customer" :
                self.handleAddToCart(self.fooditem_id, self.foodname)
            elif self.pageName == "admin" :
                self.editFoodDialog.exec()

    def handleAddToCart(self, fooditem_id, foodname) :
        pubsub.publish("addToCart", (fooditem_id, foodname))
