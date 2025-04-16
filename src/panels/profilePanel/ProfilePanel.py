import sys
import os
from src.panels.orderHPanel.OrderHPanel import QOrderHPanel

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
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
from src.components.Headers import QOtherPanelHeader
from src.components.Table import QOrderHTable
from src.panels.profilePanel.ProfileEditSection import QProfile, QProfileViewState
from PyQt6.QtCore import Qt

class QProfilePanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.order_layout.setContentsMargins(0,0,0,0)
        self.order_layout.setSpacing(0)
        history_label = QLabel("Order History")
        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,0,10)

        self.orderHTable = QOrderHTable()
        contentsVLayout.addWidget(history_label)
        contentsVLayout.addWidget(self.orderHTable)

        self.order_layout.addWidget(QOtherPanelHeader("Profile"))
        self.order_layout.addWidget(QProfile(), alignment=Qt.AlignmentFlag.AlignTop)
        self.order_layout.addLayout(contentsVLayout)

