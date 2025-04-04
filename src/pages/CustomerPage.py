import sys
import os
sys.path.append(os.path.abspath("src"))
from panels.foodPanel.FoodPanel import QFoodPanel
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


class QCustomerPage(QFrame) :
    def __init__(self):
        super().__init__()
        self.objectName = "customer"
        self.foodPanel = QFoodPanel(self.objectName)

        self.customer_layout = QVBoxLayout(self)
        self.customer_layout.addWidget(self.foodPanel)
