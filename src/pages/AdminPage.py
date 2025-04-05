import sys

from src.panels.foodPanel.FoodPanel import QFoodPanel
from src.panels.orderHPanel.OrderHPanel import QOrderHPanel
from src.panels.statsPanel.StatsPanel import QStatsPanel

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

class QAdminPage(QFrame) :
    def __init__(self):
        super().__init__()
        self.objectName = "admin"
        # will have floating footer for switch btns to panels? that possible?
        self.foodPanel = QFoodPanel(self.objectName)
        self.orderPanel = QOrderHPanel()
        self.statsPanel = QStatsPanel()
        
        self.adminStackedPanels = QStackedWidget()

        self.adminStackedPanels.addWidget(self.foodPanel)
        self.adminStackedPanels.addWidget(self.orderPanel)
        self.adminStackedPanels.addWidget(self.statsPanel)

        self.switchBtn = QPushButton("switch admin panel")
        self.switchBtn.clicked.connect(self.switchPage)

        self.admin_layout = QVBoxLayout(self)
        self.admin_layout.addWidget(self.adminStackedPanels)
        self.admin_layout.addWidget(self.switchBtn)
    
    def switchPage(self) :
        curr = self.adminStackedPanels.currentIndex()
        self.adminStackedPanels.setCurrentIndex( (curr+1) %3)