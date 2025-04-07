from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)

from src.panels.foodPanel.MenuListCont import QMenuListContainer
from src.components.SideBar import QSideBar

class QFoodPanel(QFrame) :
    def __init__(self, pageName):
        super().__init__()

        self.menuListCont = QMenuListContainer(pageName)
        
        self.food_layout = QGridLayout(self) # 
        # will have stuff

        self.food_layout.addWidget(QLabel(pageName + " food panel, put headers and stuff here"), 0, 0)
        self.food_layout.addWidget(self.menuListCont, 1, 0) 
        # design later