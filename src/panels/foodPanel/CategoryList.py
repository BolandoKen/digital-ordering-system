import sys

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

from src.panels.foodPanel.CategoryCard import QCategoryCard
from src.database.queries import fetchCatList

class QCategoryList(QFrame) : 
    # fetch all categories and list them all as btns
    # cat btns will just set stackedLists to foodlist, and update content of foodList
    def __init__(self, pageName, update_listContent, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.update_listContent = update_listContent # get update func from foodlist
        self.stackedLists = stackedLists # access parents stackedlists 
        self.catList_layout = QVBoxLayout(self)
        self.catList_layout.addWidget(QLabel("Categories"))

        self.init_catList()

        self.setStyleSheet("border: 1px solid black")

    def init_catList(self) :
        if self.pageName == "admin" :
            self.init_adminCatList()
        elif self.pageName == "customer" :
            self.init_customerCatList()

    def init_customerCatList(self) :
        self.catList = fetchCatList()
        for catTuple in self.catList :
            catCard = QCategoryCard(catTuple, self.pageName, self.update_listContent, self.stackedLists)
            self.catList_layout.addWidget(catCard)
        # no plus sign

    def init_adminCatList(self) :
        addCatBtn = QPushButton("+ add Category")
        addCatBtn.clicked.connect(self.addCategory)
        self.catList_layout.addWidget(addCatBtn)

        self.init_customerCatList()
        # has plus sign to add categories
    
    def addCategory(self) :
        print("will add category")

    def update_categoryList(self) :
        self.clear_layout(self.catList_layout)
        self.init_catList()

    def clear_layout(layout): 
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    




