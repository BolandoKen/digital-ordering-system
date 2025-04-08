
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
        self.setFixedHeight(150)
        self.setFixedWidth(150)
        self.setStyleSheet("background-color: white; color: black")
