from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)

from src.panels.foodPanel.MenuListCont import QMenuListContainer
from src.components.SideBar import QSideBar
from src.components.Headers import QFoodPanelHeader
from src.components.LineEdit import QSearchArea
from PyQt6.QtCore import Qt, QPoint, QTimer

class QFoodPanel(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.menuListCont = QMenuListContainer(pageName)

        self.food_layout = QVBoxLayout(self) # 
        self.food_layout.setContentsMargins(0,0,0,0)
        self.food_layout.setSpacing(0)

        self.food_layout.addWidget(QFoodPanelHeader(pageName))
        if pageName == "admin" :
            self.food_layout.addWidget(QSearchArea(self))
        self.food_layout.addWidget(self.menuListCont) 
        # design later