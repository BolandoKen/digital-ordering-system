import sys
import os
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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class QCategoryCard(QFrame) : # at the mean time make it a QPushBtn for simplicity
    # card for each category, display name
    def __init__(self, catTuple, pageName, update_listContent, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.category_id, self.catname, self.imgfile = catTuple
        self.update_listContent = update_listContent
        self.stackedLists = stackedLists
        self.catCard_layout = QVBoxLayout(self)

        if self.pageName == "admin" :
            self.init_adminCategoryCard()
        elif self.pageName == "customer" :
            self.init_customerCategoryCard()

        self.setStyleSheet("background-color: white; color: black")


    def init_customerCategoryCard(self) :
        self.catLabel = QLabel(self.catname)
        self.catimg = QLabel()
        self.setPixMapOf(self.catimg, self.imgfile)
      
        self.catCard_layout.addWidget(self.catLabel)
        self.catCard_layout.addWidget(self.catimg)
        # no edit/del btns

    def init_adminCategoryCard(self) :
        self.init_customerCategoryCard()
        self.catCard_layout.addWidget(QPushButton("edit"))
        self.catCard_layout.addWidget(QPushButton("delete"))
        # has edit/del btns , edit/trash icons in the card

    def setPixMapOf(self, label, imgFileName) :
        if imgFileName is None:
            imgFileName = "icecream.png"
        path = os.path.join(os.path.abspath("assets/foodimg"), imgFileName) 
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(50,50)
        label.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.catCardClicked()

    def catCardClicked(self) :
        self.update_listContent(self.category_id, self.catname)
        self.stackedLists.setCurrentIndex(1)