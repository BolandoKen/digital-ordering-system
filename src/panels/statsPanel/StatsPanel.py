import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from PyQt6.QtCore import Qt
from src.database.queries import fetchStatistics
from src.components.Headers import QOtherPanelHeader
from src.components.Table import QStatsTable

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.stats_layout.setContentsMargins(0,0,0,0)
        self.stats_layout.setSpacing(0)
        self.mostordered = True
        self.page_setup()

    def page_setup(self):
   
        self.stats_layout.addWidget(QOtherPanelHeader("Statistics"))
        queryBarHLayout = QHBoxLayout()
        self.sort_btn = QPushButton("Show Least Ordered")
        self.sort_btn.clicked.connect(self.changeorder)
        queryBarHLayout.addWidget(self.sort_btn)
        queryBarHLayout.addStretch()
        queryBarHLayout.addWidget(QPushButton("filter"))
        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,0,10)
        contentsVLayout.setSpacing(5)

        self.table = QStatsTable()
        contentsVLayout.addLayout(queryBarHLayout)
        contentsVLayout.addWidget(self.table)
        self.stats_layout.addLayout(contentsVLayout)
    
    def changeorder(self):
        self.mostordered = not self.mostordered
        if self.mostordered:
            self.sort_btn.setText("Show Least Ordered")
        else:
            self.sort_btn.setText("Show Most Ordered")
        
        self.table.statistics_table(self.mostordered)

    #Still have to make handleSubmitOrderClicked actually send the data into the database (orderitems is empty)