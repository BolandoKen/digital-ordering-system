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
from src.panels.foodPanel.CategoryList import QCategoryList
from src.panels.foodPanel.FoodList import QFoodList
from src.utils.PubSub import pubsub

class QMenuListContainer(QFrame) :
    # contain the stacked lists
    def __init__(self, pageName) :
        super().__init__()
        self.listCont_layout = QVBoxLayout(self)
        self.listCont_layout.setContentsMargins(0,0,0,0)

        self.stackedLists = QStackedWidget()
        self.foodList = QFoodList(pageName, self.stackedLists)
        self.categoryList = QCategoryList(pageName,self.stackedLists)

        self.stackedLists.addWidget(self.categoryList)
        self.stackedLists.addWidget(self.foodList)
        
        self.listCont_layout.addWidget(self.stackedLists)
        pubsub.subscribe(f"{pageName}_catCardClicked", self.switchToFoodPanel)
        pubsub.subscribe(f"{pageName}_backToCatClicked", self.switchToCatPanel)
        
    def switchToFoodPanel(self, e = None) :
        self.stackedLists.setCurrentIndex(1)

    def switchToCatPanel(self, e = None) :
        self.stackedLists.setCurrentIndex(0)