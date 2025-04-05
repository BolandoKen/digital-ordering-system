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

from src.panels.foodPanel.MenuListCont import QMenuListContainer

class QFoodPanel(QFrame) :
    def __init__(self, pageName):
        super().__init__()

        self.menuListCont = QMenuListContainer(pageName)

        self.food_layout = QVBoxLayout(self) # refactor to grid later on
        # will have stuff

        self.food_layout.addWidget(QLabel(pageName + " food panel, put headers and stuff here"))
        self.food_layout.addWidget(self.menuListCont) 
        # self.food_layout add (ordercart widget) # will have order cart side bar here