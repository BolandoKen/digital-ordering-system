import sys

from PyQt6.QtCore import Qt
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

from src.database.queries import fetchOrderHistory

class QOrderHPanel(QFrame) : # not used
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["OrderID", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.order_layout.addWidget(self.table)
        self.add_sample_data()
    
    def add_sample_data(self):
        orders = fetchOrderHistory()
        self.table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            order_id, order_datetime = order
            self.table.setItem(row, 1, QTableWidgetItem(str(order_datetime)))
            self.table.setItem(row, 0, QTableWidgetItem(str(order_id)))
    