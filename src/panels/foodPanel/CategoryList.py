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
    QScrollArea
)
from src.utils.PubSub import pubsub
from src.panels.foodPanel.CategoryCard import QCategoryCard
from src.database.queries import fetchCatList
from src.components.Dialogs import QaddDialog, QeditDialog
from PyQt6.QtCore import Qt
from src.components.ScrollArea import QScrollAreaLayout
from src.components.FlowLayout import QFlowLayout
from src.components.Buttons import QAddButton

class QCategoryList(QFrame) : 
    def __init__(self, pageName,stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.stackedLists = stackedLists # access parents stackedlists 
        self.catCardMap = {}
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.catList_Layout = QScrollAreaLayout(QFlowLayout, self.scroll_layout)
    
        self.addCatDialog = QaddDialog("category", self.window())
        self.editCatDialog = QeditDialog("category", self.window())
        pubsub.subscribe("updateCategory", self.update_categoryList)
        if pageName == "admin" : 
            pubsub.subscribe("catedit_clicked", self.initEditDialog)
        self.init_catList()

        # will listen to search , subscribe category searched
        # cat id will be passed down, using catCardMap, we ensure visible the card
        # redirect (setindex) -> ensure visible

    def initEditDialog(self, Tuple) :
        self.editCatDialog.init_editCategory(Tuple)
        self.editCatDialog.exec()

    def init_catList(self) :
        if self.pageName == "admin" :
            self.init_adminCatList()
        elif self.pageName == "customer" :
            self.init_customerCatList()

    def init_customerCatList(self) :
        self.catList = fetchCatList(self.pageName)
        for catTuple in self.catList :
            catCard = QCategoryCard(catTuple, self.pageName, self.stackedLists)
            self.catCardMap[str(catTuple[0])] = catCard
            self.catList_Layout.addWidget(catCard)
        # no plus sign

    def init_adminCatList(self) :
        addCatBtn = QAddButton()
        addCatBtn.connectTo(self.handleAddCategory)
        self.catList_Layout.addWidget(addCatBtn)

        self.init_customerCatList()
        # has plus sign to add categories
    
    def handleAddCategory(self) :
        self.addCatDialog.exec()

    def update_categoryList(self, e = None) :
        print("updated",self.pageName)
        self.clear_layout(self.catList_Layout.getLayout())
        self.catList_Layout.myLayout.invalidate()
        self.init_catList()
        self.catList_Layout.myLayout.invalidate()

    def clear_layout(self, layout): 
        print('rerendered category list from ', self.pageName)
        self.catCardArr = {}
        if layout is not None:
            for i in reversed(range(layout.count())): # reverse, because deletion fills gaps
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   
    




