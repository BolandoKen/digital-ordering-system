import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent #chatgpt'd, idk how to do relative file path
panels_dir = current_dir.parent     
sys.path.append(str(panels_dir))
from orderHPanel.OrderHPanel import QOrderHPanel

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

class QProfilePanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.setPixMapOf(self.image_label, "icecream.png")        
        name_label = QLabel("M's Kitchen")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(100)
        history_label = QLabel("Order History")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.history_panel = QOrderHPanel()
        scroll_area.setWidget(self.history_panel)
        self.order_layout.addWidget(self.image_label)
        self.order_layout.addWidget(name_label)
        self.order_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.order_layout.addWidget(history_label)
        self.order_layout.addWidget(scroll_area)

    def setPixMapOf(self, label, imgFileName): #from FoodCard.py
        if imgFileName is None :
            imgFileName = "icecream.png"
        path = os.path.join(os.path.abspath("assets/foodimg"), imgFileName) 
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(150,150)
        label.setScaledContents(True)

