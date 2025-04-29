
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect

)
from PyQt6.QtGui import QPixmap, QColor

class QMenuCard(QFrame) :
    def __init__(self):
        super().__init__()
        self.setFixedHeight(225)
        self.setFixedWidth(225)
        self.setObjectName("MenuCard")
        self.setStyleSheet("""
            #MenuCard{
            background-color: white;
            padding: 0px;
            color: black;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;
            }
                           
            #MenuCard * 
            {
            background-color: white;
            color:black;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)
    

# make class card for add buttons