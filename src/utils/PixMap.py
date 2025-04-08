import os
from PyQt6.QtGui import QPixmap

def setPixMapOf(label, imgFileName) :
    if imgFileName is None:
        imgFileName = "icecream.png"
    path = os.path.join(os.path.abspath("assets/foodimg"), imgFileName) 
    pixmap = QPixmap(path)
    label.setPixmap(pixmap)
    label.setFixedSize(50,50)
    label.setScaledContents(True)