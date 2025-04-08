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

class QFoodItemCard(QFrame) : # at the mean time make it a QPushBtn for simplicity
    # card for each food item, display name, img, price
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
        self.editBtn = QPushButton("edit")
        self.editBtn.clicked.connect(self.editFoodDialog.exec)
        self.foodCard_layout.addWidget(self.editBtn)
        self.delBtn = QPushButton("delete")
        self.delBtn.clicked.connect(self.handleFoodDel)
        self.foodCard_layout.addWidget(self.delBtn)

        # has edit/del btns , edit/trash icons in the card



    def handleFoodDel(self) :
        deleteFoodItem(self.fooditem_id)
        pubsub.publish("updateFoodItem")

    def mousePressEvent(self, event):
        if self.pageName == "admin" : 
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.handleAddToCart(self.fooditem_id, self.foodname)

    def handleAddToCart(self, fooditem_id, foodname) :
        # can do self.parent() now yay
        # publish to pubsub
        pubsub.publish("addToCart", (fooditem_id, foodname))
        # self.parent().parent().parent().parent().parent().sideBar.handleFoodAddToCart(fooditem_id, foodname)
