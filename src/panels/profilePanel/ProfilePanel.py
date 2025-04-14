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

class QProfilePanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.order_layout.setContentsMargins(0,0,0,0)
        self.order_layout.setSpacing(0)
        self.image_label = QLabel()
        setPixMapOf(self.image_label, "icecream.png", "food")        
        name_label = QLabel("M's Kitchen")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(100)
        history_label = QLabel("Order History")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.history_panel = QOrderHPanel()
        scroll_area.setWidget(self.history_panel)
        self.order_layout.addWidget(QOtherPanelHeader("Profile"))
        self.order_layout.addWidget(self.image_label)
        self.order_layout.addWidget(name_label)
        self.order_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.order_layout.addWidget(history_label)
        self.order_layout.addWidget(scroll_area)

