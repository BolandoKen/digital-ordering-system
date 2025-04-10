
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

class QMenuCard(QFrame) :
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: white; color: black")