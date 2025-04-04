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

class QCustomerPage(QFrame) :
    def __init__(self):
        super().__init__()