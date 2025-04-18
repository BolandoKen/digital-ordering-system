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
from src.components.ComboBox import QCatComboBox

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.stats_layout.setContentsMargins(0,0,0,0)
        self.stats_layout.setSpacing(0)
        self.mostordered = True
        self.stats_setup()

    def stats_setup(self):
   
        self.stats_layout.addWidget(QOtherPanelHeader("Statistics"))
        queryBarHLayout = QHBoxLayout()
        self.sort_btn = QPushButton("Show Least Ordered")
        self.sort_btn.clicked.connect(self.changeorder)
        queryBarHLayout.addWidget(self.sort_btn)
        queryBarHLayout.addStretch()
        self.catComboBox = QCatComboBox("stat")
        self.catComboBox.currentIndexChanged.connect(self.update_table)
        queryBarHLayout.addWidget(self.catComboBox)
        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,0,10)
        contentsVLayout.setSpacing(5)

        self.table = QStatsTable() 
        # on combobox change update stats table, make function inside to handle it
        # check edit dialog, access category_id by self.categoryidComboBox.itemData(self.categoryidComboBox.currentIndex())
        # combobox has displayed value (category name) and inner value (category id)
        # we take inner value to query into sql
        contentsVLayout.addLayout(queryBarHLayout)
        contentsVLayout.addWidget(self.table)
        self.stats_layout.addLayout(contentsVLayout)
        self.update_table()
    
    def changeorder(self):
        self.mostordered = not self.mostordered
        if self.mostordered:
            self.sort_btn.setText("Show Least Ordered")
        else:
            self.sort_btn.setText("Show Most Ordered")
        
        self.update_table()

    def update_table(self):
        category_id = self.catComboBox.itemData(self.catComboBox.currentIndex())
        if category_id == None or category_id == "no filter":
            category_id = None
        
        self.table.updateStatsTable(category_id, self.mostordered)
    
