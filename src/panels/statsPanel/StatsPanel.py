import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
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

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.mostordered = True
        self.page_setup()
        self.statistics_table()

    def page_setup(self):
        title = QLabel("Statistics Panel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("background-color: white; color: black")
        self.stats_layout.addWidget(title)
        self.toggle_btn = QPushButton("Show Least Ordered")
        self.toggle_btn.clicked.connect(self.changeorder)
        self.stats_layout.addWidget(self.toggle_btn)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Food", "Category", "Times Ordered"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_layout.addWidget(self.table)

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
            self.toggle_btn.setText("Show Least Ordered")
        else:
            self.toggle_btn.setText("Show Most Ordered")
        
        self.statistics_table()

    #Still have to make handleSubmitOrderClicked actually send the data into the database (orderitems is empty)