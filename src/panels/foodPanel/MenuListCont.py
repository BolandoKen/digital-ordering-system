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


class QMenuListContainer(QFrame) :
    # contain the stacked lists
    def __init__(self, pageName) :
        super().__init__()
        self.listCont_layout = QVBoxLayout(self)
        self.stackedLists = QStackedWidget()
        self.foodList = QFoodList(pageName, self.stackedLists)
        update_listContent = self.foodList.update_listContent
        self.categoryList = QCategoryList(pageName,update_listContent, self.stackedLists)

        self.stackedLists.addWidget(self.categoryList)
        self.stackedLists.addWidget(self.foodList)
        
        self.listCont_layout.addWidget(QLabel("imagine a container of the menu"))
        self.listCont_layout.addWidget(self.stackedLists)

