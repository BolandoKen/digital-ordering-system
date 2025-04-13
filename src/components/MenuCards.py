
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
# make class card for add buttons