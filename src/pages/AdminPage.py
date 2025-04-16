import sys

from src.panels.foodPanel.FoodPanel import QFoodPanel
from src.panels.statsPanel.StatsPanel import QStatsPanel
from src.panels.profilePanel.ProfilePanel import QProfilePanel

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

class QAdminPage(QFrame) :
    def __init__(self):
        super().__init__()
        self.objectName = "admin"
        self.foodPanel = QFoodPanel(self.objectName)
        self.statsPanel = QStatsPanel()
        self.profilePanel = QProfilePanel()
        
        self.adminStackedPanels = QStackedWidget()
        self.sideBar = QSideBar(self.objectName, self.switchPage)
        self.logoHeader = QLogoHeader("admin")

        self.adminStackedPanels.addWidget(self.foodPanel)
        self.adminStackedPanels.addWidget(self.statsPanel)
        self.adminStackedPanels.addWidget(self.profilePanel)

        self.admin_layout = QGridLayout(self)
        self.admin_layout.setSpacing(0)
        self.admin_layout.setContentsMargins(0,0,0,0)
        self.admin_layout.addWidget(self.logoHeader, 0,0)
        self.admin_layout.addWidget(self.adminStackedPanels, 1, 0)
        self.admin_layout.addWidget(self.sideBar, 0, 1, 2, 1)


    def switchPage(self) :
        curr = self.adminStackedPanels.currentIndex()
        self.adminStackedPanels.setCurrentIndex( (curr+1) %3)