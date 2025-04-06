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
)

class QProfilePanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.order_layout.addWidget(QLabel("admin profile panel"))

