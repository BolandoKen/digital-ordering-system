import sys
from PyQt6.QtWidgets import (
   QApplication,
   QWidget,
   QLabel,
   QHBoxLayout,
   QVBoxLayout,
   QPushButton
)
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtCore import QSize, Qt
from src.components.Buttons import QEditButton
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy


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
        self.setFixedWidth(120)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        green_dot = CatStatus("green", 10)  
        available_Count = QLabel(str(available_items)) 
        available_Count.setStyleSheet("""
                                      font: 'Helvetica';
                                      font-size: 20px;
                                      font-weight: bold;
                                      """)
        layout.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(green_dot)
        layout.addWidget(available_Count)

        red_dot = CatStatus("red", 10) 
        unavailable_Count = QLabel(str(unavailable_items)) 
        unavailable_Count.setStyleSheet("""
                                        font: 'Helvetica';
                                        font-size: 20px;
                                        font-weight: bold;
                                        """)
        layout.addWidget(red_dot)
        layout.addWidget(unavailable_Count)

        emptyCategoryLabel = QLabel("empty category")
        emptyCategoryLabel.setStyleSheet("""
                                         font: "Helvetica";
                                         """)
        layout.addWidget(emptyCategoryLabel)
        emptyCategoryLabel.hide()
        self.setLayout(layout)
        layout.addStretch()

        if (available_items == 0 ) : 
            green_dot.hide()
            available_Count.hide()
        if (unavailable_items == 0 ) : 
            red_dot.hide()
            unavailable_Count.hide()
        if (available_items == 0 and unavailable_items == 0) :
            emptyCategoryLabel.show()
        # add logic here, if label is 0, hide that label and status


class QCatStatusEditLayout(QHBoxLayout) :
    def __init__(self, availableItemCount, unavailableItemCount, editCb) :
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.addWidget(QStatusIndicator(availableItemCount, unavailableItemCount))
        self.addStretch()
        self.editBtn = QEditButton() 
        self.addWidget(self.editBtn)
        self.editBtn.clicked.connect(editCb)