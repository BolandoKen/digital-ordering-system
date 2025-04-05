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

class QCategoryList(QFrame) : 
    # fetch all categories and list them all as btns
    # cat btns will just set stackedLists to foodlist, and update content of foodList
    def __init__(self, pageName, update_listContent, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.update_listContent = update_listContent # get update func from foodlist
        self.stackedLists = stackedLists # access parents stackedlists 
        self.catList_layout = QVBoxLayout(self)
        self.mockCatArr = ["Seafood", "Beverage"]
        self.catList_layout.addWidget(QLabel("imagine list of categories btn"))
        if self.pageName == "admin" :
            self.init_adminCatList()
        elif self.pageName == "customer" :
            self.init_customerCatList()

    def init_customerCatList(self) :
        for cat in self.mockCatArr :
            adminMockBtn = QCategoryCard(cat, self.pageName)
            adminMockBtn.clicked.connect(self.cardClicked) # put cardClicked in this class to avoid deeper passes
            self.catList_layout.addWidget(adminMockBtn)
        # no plus sign

    def init_adminCatList(self) :
        addCatBtn = QPushButton("+ add Category")
        addCatBtn.clicked.connect(self.addCategory)
        self.catList_layout.addWidget(addCatBtn)

        self.init_customerCatList()
        # has plus sign to add categories
    
    def addCategory(self) :
        print("will add category")

    def cardClicked(self) :
        category = self.sender().text()
        self.update_listContent(category)
        self.stackedLists.setCurrentIndex(1)



