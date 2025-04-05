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
from src.panels.foodPanel.FoodCard import QFoodItemCard
from PyQt6.QtGui import QPixmap

class QFoodList(QFrame) :
    # fetch all food items under the category, and list them all as btns
    # food btns on click will add to order cart
    def __init__(self, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.stackedLists = stackedLists
        self.foodList_layout = QVBoxLayout(self)
        self.mockFoodlist = {
            "Seafood" : ["salamander", "shrimp", "tuna", "egg"],
            "Beverage" : ["coke", "water", "sprite"]
        }
        simulate_preloads() # preloading is just impossible, very slow..
    # optimize... pixmap is rly expensive, must preload all qfoodcards?
    # no, just cache them.. make own caching system ...  
    def update_listContent(self, category) :
        clear_layout(self.foodList_layout) 
        self.headTitle = QLabel("")
        self.backBtn = QPushButton("<- back to cat list") 
        self.backBtn.clicked.connect(self.backToCat)
        self.foodList_layout.addWidget(self.headTitle)
        self.foodList_layout.addWidget(self.backBtn)
        self.category = category
        if self.pageName == "admin" :
            self.init_adminFoodList()
        elif self.pageName == "customer" :
            self.init_customerFoodList()

        self.headTitle.setText(f"imagine list of fooditems under {self.category}")
        # updates the list content

    def init_customerFoodList(self) :
        foodlist = self.mockFoodlist[self.category]
        for item in foodlist :
            foodCard = QFoodItemCard(item, self.pageName)
            self.foodList_layout.addWidget(foodCard)
        # no plus sign, unable to add

    def init_adminFoodList(self) :
        addFoodBtn = QPushButton("+ add food item")
        addFoodBtn.clicked.connect(self.addFoodItem)
        self.foodList_layout.addWidget(addFoodBtn)

        self.init_customerFoodList()
        # plus sign to add food under category
    
    def addFoodItem(self) :
        print(f"will add food under {self.category}")

    def backToCat(self) :
        self.stackedLists.setCurrentIndex(0)

def clear_layout(layout): 
    if layout is not None:
        for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
            item = layout.takeAt(i) 
            if item.widget(): 
                item.widget().deleteLater()
            elif item.spacerItem():  
                layout.removeItem(item) 

def simulate_preloads() :
    start_time = time.time()
    for i in range(50) :
        path = os.path.join(os.path.abspath("assets/foodimg"), "icecream.jpg")
        pixmap = QPixmap(path)
    print("--- %s seconds ---" % (time.time() - start_time))
