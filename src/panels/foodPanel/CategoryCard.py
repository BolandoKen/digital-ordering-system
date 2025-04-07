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
from src.utils.PubSub import pubsub
from src.database.Categories import deleteCategory
from src.components.Dialogs import QeditDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class QCategoryCard(QFrame) : # at the mean time make it a QPushBtn for simplicity
    # card for each category, display name
    def __init__(self, catTuple, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.category_id, self.catname, self.imgfile = catTuple
        self.editCatDialog = QeditDialog("category", catTuple)
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
        self.editBtn = QPushButton("edit")
        self.editBtn.clicked.connect(self.editCatDialog.exec)
        self.catCard_layout.addWidget(self.editBtn)
        self.delBtn = QPushButton("delete")
        self.delBtn.clicked.connect(self.handleCatDelete)
        self.catCard_layout.addWidget(self.delBtn)
        # has edit/del btns , edit/trash icons in the card

    def setPixMapOf(self, label, imgFileName) :
        if imgFileName is None:
            imgFileName = "icecream.png"
        path = os.path.join(os.path.abspath("assets/foodimg"), imgFileName) 
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(50,50)
        label.setScaledContents(True)

    def handleCatDelete(self) :
        deleteCategory(self.category_id)
        pubsub.publish("updateCategory")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.handleCatCardClicked()

    def handleCatCardClicked(self) :
        pubsub.publish("catCardClicked", (self.category_id, self.catname))
        # self.update_listContent(self.category_id, self.catname)
        self.stackedLists.setCurrentIndex(1)
    
