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
)
import time
from src.utils.PubSub import pubsub
from src.panels.foodPanel.FoodCard import QFoodItemCard
from src.components.Dialogs import QaddDialog
from src.database.queries import fetchFoodUnderCatList
from PyQt6.QtGui import QPixmap

class QFoodList(QFrame) :
    # fetch all food items under the category, and list them all as btns
    # food btns on click will add to order cart
    def __init__(self, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.stackedLists = stackedLists
        self.foodList_layout = QVBoxLayout(self)
        self.showUnavailable = False
        self.addFoodDialog = QaddDialog("food")
        if self.pageName == "admin" :
            pubsub.subscribe("admin_catCardClicked", self.update_listContent)
        elif self.pageName == "customer" :
            pubsub.subscribe("customer_catCardClicked", self.update_listContent)
        pubsub.subscribe("updateFoodItem", self.update_listContent)

    def init_customerFoodList(self) :
        foodlist = fetchFoodUnderCatList(self.category_id, self.showUnavailable)
        for foodTuple in foodlist :
            foodCard = QFoodItemCard(foodTuple, self.pageName)
            self.foodList_layout.addWidget(foodCard)
        self.foodList_layout.addStretch()
        # no plus sign, unable to add

    def init_adminFoodList(self) :
        addFoodBtn = QPushButton("+ add food item")
        self.showUnBtn = QPushButton()
        if self.showUnavailable :
            self.showUnBtn.setText("hide unavailable items") # his doesnt work why?
        else :
            self.showUnBtn.setText("show unavailable items")
        self.showUnBtn.clicked.connect(self.toggleShowUnavailable)
        addFoodBtn.clicked.connect(self.addFoodItem)
        self.foodList_layout.addWidget(addFoodBtn)
        self.foodList_layout.addWidget(self.showUnBtn)

        self.init_customerFoodList()
        # plus sign to add food under category

    
    def update_listContent(self, catTuple = None) :
        if catTuple is not None :
            category_id, catname = catTuple
            self.category_id = category_id
            self.catname = catname
        self.clear_layout(self.foodList_layout) 
        self.headTitle = QLabel("")
        self.headTitle.setFixedHeight(50)
        self.backBtn = QPushButton("<- back to cat list") 
        self.backBtn.clicked.connect(self.backToCat)

        self.foodList_layout.addWidget(self.headTitle)
        self.foodList_layout.addWidget(self.backBtn)

        if self.pageName == "admin" :
            self.init_adminFoodList()
        elif self.pageName == "customer" :
            self.init_customerFoodList()
        
        self.headTitle.setText(self.catname)
        # updates the list content

    def addFoodItem(self) :
        self.addFoodDialog.category_id = self.category_id
        self.addFoodDialog.exec()

    def backToCat(self) :
        self.stackedLists.setCurrentIndex(0)
    
    def toggleShowUnavailable(self) :
        self.showUnavailable = not self.showUnavailable
        self.update_listContent()

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)     


