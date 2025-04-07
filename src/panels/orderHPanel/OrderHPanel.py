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

class QOrderHPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        title_label = QLabel("Order History")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Date", "Order ID"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.order_layout.addWidget(title_label)
        self.order_layout.addWidget(self.table)
        self.add_sample_data()
    
    def add_sample_data(self):
        self.table.setRowCount(3)
        self.table.setItem(0, 0, QTableWidgetItem("Day 1"))
        self.table.setItem(0, 1, QTableWidgetItem("sumthing sumething"))
        self.table.setItem(1, 0, QTableWidgetItem("Day 2"))
        self.table.setItem(1, 1, QTableWidgetItem("fried chiken"))
        self.table.setItem(2, 0, QTableWidgetItem("Day 3"))
        self.table.setItem(2, 1, QTableWidgetItem("buh buh"))
        

