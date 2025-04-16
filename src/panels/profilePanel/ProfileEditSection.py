import sys
import os
from src.panels.orderHPanel.OrderHPanel import QOrderHPanel

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
    QVBoxLayout,
    QScrollArea
)
from src.utils.PixMap import setPixMapOf

class QProfileEdit(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.inner_VLayout = QVBoxLayout()
        self.profileIcon = QLabel()
        setPixMapOf(self.profileIcon, "pfp_icon.svg", "icon")
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.main_layout.addWidget(self.profileIcon)
        self.main_layout.addLayout(self.inner_VLayout)
        self.init_default()
        
    def init_default(self) :
        self.inner_VLayout.addWidget(QLabel("M's Kitchen"))

