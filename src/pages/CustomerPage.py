from src.panels.foodPanel.FoodPanel import QFoodPanel
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QGridLayout,
)
from src.components.SideBar import QSideBar
from src.components.Headers import QLogoHeader


class QCustomerPage(QFrame) :
    def __init__(self):
        super().__init__()
        self.objectName = "customer"
        self.foodPanel = QFoodPanel(self.objectName)
        self.sideBar = QSideBar(self.objectName)
        self.logoHeader = QLogoHeader("customer")
        self.customer_layout = QGridLayout(self)
        self.customer_layout.setSpacing(0)
        self.customer_layout.setContentsMargins(0,0,0,0)
        self.customer_layout.addWidget(self.logoHeader, 0,0)
        self.customer_layout.addWidget(self.foodPanel, 1, 0)
        self.customer_layout.addWidget(self.sideBar, 0, 1, 2, 1)
