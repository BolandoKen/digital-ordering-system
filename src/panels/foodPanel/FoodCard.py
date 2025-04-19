import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QLineEdit,
    QSpinBox,
    QMessageBox
)
from src.components.Dialogs import QeditDialog, QConfirmDialog
from src.database.FoodItems import deleteFoodItem, reviveFoodItem
from src.utils.PubSub import pubsub
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from src.utils.PixMap import setPixMapOf
from src.components.MenuCards import QMenuCard
from src.components.Buttons import QDeleteButton
from src.database.queries import checkFoodHasBeenOrdered

class QFoodItemCard(QMenuCard) : 
    def __init__(self, foodTuple, pageName) : 
        super().__init__()
        self.pageName = pageName
        self.fooditem_id, self.foodname, self.price, self.imgfile, self.is_available, self.category_id = foodTuple
        self.foodCard_layout = QVBoxLayout(self)
        self.hasBeenOrdered = checkFoodHasBeenOrdered(self.fooditem_id)
        if self.pageName == "admin" :
            self.editFoodDialog = QeditDialog("food", foodTuple, self.window())
            self.init_adminFoodItemCard()
        elif self.pageName == "customer" :
            self.init_customerFoodItemCard()

    def init_customerFoodItemCard(self) :
        # no edit/del btns
        self.foodLabel = QLabel(self.foodname)
        self.foodimg = QLabel()
        self.foodimgpixmap = setPixMapOf(self.foodimg, self.imgfile, "food")["pixmap"]
        self.priceLabel = QLabel(str(self.price))   
             
        self.foodCard_layout.addWidget(self.foodimg, alignment=Qt.AlignmentFlag.AlignCenter) 
        self.foodCard_layout.addWidget(self.foodLabel, alignment=Qt.AlignmentFlag.AlignCenter)   
        self.foodCard_layout.addWidget(self.priceLabel, alignment=Qt.AlignmentFlag.AlignCenter)

    def init_adminFoodItemCard(self) :
        # has edit/del btns , edit/trash icons in the card
        self.init_customerFoodItemCard()
        delHBoxLayout = QHBoxLayout()
        delHBoxLayout.setContentsMargins(0,0,0,0)
        delHBoxLayout.addStretch()
        self.delBtn = QDeleteButton()
        self.delBtn.clicked.connect(self.handleFoodDel)
        delHBoxLayout.addWidget(self.delBtn)
        self.foodCard_layout.insertLayout(0,delHBoxLayout)
        if self.hasBeenOrdered :
            if self.is_available  :
                self.delBtn.setState("unavailable") # diff icons instead of text
            else :
                self.delBtn.setState("revive")
        else :
            self.delBtn.setState("delete")
        # note : its bad to subscribe pubsub for temporary elements

    # : will have different icons for deletes, card will have different state
    # orders will emit setState functions, 

    def handleFoodDel(self) :
        # if food is available : delete or hide
        # if food is unavailable : show
        typeOf = "delete"
        message = "Are you sure you want to delete this food item?"

        if self.hasBeenOrdered and not self.is_available:
            message = "Are you sure you want to revive this food item?"
            typeOf = "revive"
        elif self.hasBeenOrdered:
            message = "This item has existing orders in order history. It will be hidden instead of deleted."

        confirm = QConfirmDialog("Confirm", message, self)
        if confirm.exec():  # returns True if "Yes" was clicked
            if typeOf == "delete":
                deleteFoodItem(self.fooditem_id)
            elif typeOf == "revive":
                reviveFoodItem(self.fooditem_id)
            pubsub.publish("updateFoodItem")
            pubsub.publish("updateCategory")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.pageName == "customer" :
                self.handleAddToCart(self.fooditem_id, self.foodname, self.foodimgpixmap, self.price)
            elif self.pageName == "admin" :
                self.editFoodDialog.exec()

    def handleAddToCart(self, fooditem_id, foodname,imgpixmap, price) :
        pubsub.publish("addToCart", (fooditem_id, foodname, imgpixmap, price))
