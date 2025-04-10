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
from src.components.ScrollArea import QScrollAreaLayout
from src.components.FlowLayout import QFlowLayout

class QFoodList(QFrame) :

    def __init__(self, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.stackedLists = stackedLists
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.foodList_layout = QScrollAreaLayout(QFlowLayout, self.scroll_layout)

        self.showUnavailable = False
        self.addFoodDialog = QaddDialog("food")
        pubsub.subscribe(f"{self.pageName}_catCardClicked", self.update_listContent)
        self.subbedToUpdate = False
        self.subbedToToggle = False
        # make separete subscribe function? like init_subscribe
    def init_customerFoodList(self) :
        foodlist = fetchFoodUnderCatList(self.category_id, self.showUnavailable)
        for foodTuple in foodlist :
            foodCard = QFoodItemCard(foodTuple, self.pageName)
            self.foodList_layout.addWidget(foodCard)
        
        # no plus sign, unable to add

    def init_adminFoodList(self) :
        addFoodBtn = QPushButton("+ add food item")
        addFoodBtn.clicked.connect(self.handleAddFoodItem)
        self.foodList_layout.addWidget(addFoodBtn)
        if not self.subbedToToggle :
            pubsub.subscribe("admin_toggleShowUnavailable", self.toggleShowUnavailable)
            pubsub.subscribe("orderSubmitted_event", self.update_listContent)
            self.subbedToToggle = True
        self.init_customerFoodList()

        # pubsub.subscribe("orderSubmitted_event", self.setState)
        # plus sign to add food under category

    
    def update_listContent(self, catTuple = None) :
        if self.subbedToUpdate is False :
            pubsub.subscribe("updateFoodItem", self.update_listContent)
            self.subbedToUpdate = True
            
        if catTuple is not None :
            category_id, catname = catTuple
            self.category_id = category_id
            self.catname = catname
        self.clear_layout(self.foodList_layout.getLayout()) 

        if self.pageName == "admin" :
            self.init_adminFoodList()
        elif self.pageName == "customer" :
            self.init_customerFoodList()
        
        # updates the list content

    def handleAddFoodItem(self) :
        self.addFoodDialog.category_id = self.category_id
        self.addFoodDialog.exec()
    
    def toggleShowUnavailable(self, e = None) :
        self.showUnavailable = not self.showUnavailable

        self.update_listContent()

    def clear_layout(self, layout): 
        print('rerender from', self.pageName)
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)     


