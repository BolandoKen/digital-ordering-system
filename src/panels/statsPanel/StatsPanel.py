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

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.stats_layout.setContentsMargins(0,0,0,0)
        self.stats_layout.setSpacing(0)
        self.mostordered = True
        self.page_setup()
        self.statistics_table()

    def page_setup(self):
   
        self.stats_layout.addWidget(QOtherPanelHeader("Statistics"))
        queryBarHLayout = QHBoxLayout()
        self.sort_btn = QPushButton("Show Least Ordered")
        self.sort_btn.clicked.connect(self.changeorder)
        queryBarHLayout.addWidget(self.sort_btn)
        queryBarHLayout.addStretch()
        queryBarHLayout.addWidget(QPushButton("filter"))
        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,10,10)
        contentsVLayout.setSpacing(5)

        self.table = QTableWidget()
        contentsVLayout.addLayout(queryBarHLayout)
        contentsVLayout.addWidget(self.table)
        self.stats_layout.addLayout(contentsVLayout)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Food", "Category", "Times Ordered"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def statistics_table(self):
        stats_data = fetchStatistics('DESC' if self.mostordered else 'ASC')
        self.table.setRowCount(len(stats_data))
        for row, (food, category, times) in enumerate(stats_data): 
            self.table.setItem(row, 0, QTableWidgetItem(food))
            self.table.setItem(row, 1, QTableWidgetItem(category))
            self.table.setItem(row, 2, QTableWidgetItem(str(times)))
    
    def changeorder(self):
        self.mostordered = not self.mostordered
        if self.mostordered:
            self.sort_btn.setText("Show Least Ordered")
        else:
            self.sort_btn.setText("Show Most Ordered")
        
        self.statistics_table()

    #Still have to make handleSubmitOrderClicked actually send the data into the database (orderitems is empty)