import sys
from PyQt6.QtWidgets import (
   QApplication,
   QWidget,
   QLabel,
   QHBoxLayout,
   QVBoxLayout
)
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtCore import QSize, Qt

class CatStatus(QLabel):
    def __init__(self, color, size=10):
        super().__init__()
        self.setFixedSize(QSize(size, size))
        self.setPixmap(self.create_dot(color, size))  

    def create_dot(self, color, size):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent) 
        painter = QPainter(pixmap)
        painter.setBrush(QColor(color)) 
        painter.setPen(Qt.PenStyle.NoPen)  
        painter.drawEllipse(0, 0, size, size)  
        painter.end()
        return pixmap

class QStatusIndicator(QWidget):
    def __init__(self, available_items=0, unavailable_items=0):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        green_dot = CatStatus("green", 10)  
        available_Count = QLabel(str(available_items)) 
        layout.addWidget(green_dot)
        layout.addWidget(available_Count)

        red_dot = CatStatus("red", 10) 
        unavailable_Count = QLabel(str(unavailable_items)) 
        layout.addWidget(red_dot)
        layout.addWidget(unavailable_Count)

        self.setLayout(layout)
