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

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.stats_layout.addWidget(QLabel("admin stats panel"))
