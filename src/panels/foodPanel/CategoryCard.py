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
from src.utils.PixMap import setPixMapOf
from src.components.MenuCards import QMenuCard

class QCategoryCard(QMenuCard) :
    def __init__(self, catTuple, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.category_id, self.catname, self.imgfile = catTuple
        self.editCatDialog = QeditDialog("category", catTuple)
        self.stackedLists = stackedLists
        self.catCard_layout = QVBoxLayout(self)

        if self.pageName == "admin" :
            self.publishClickedEvent = "admin_catCardClicked"
            self.init_adminCategoryCard()
        elif self.pageName == "customer" :
            self.publishClickedEvent = "customer_catCardClicked"
            self.init_customerCategoryCard()


    def init_customerCategoryCard(self) :
        # no edit/del btns
        self.catLabel = QLabel(self.catname)
        self.catimg = QLabel()
        setPixMapOf(self.catimg, self.imgfile, "category") 
    
        self.catCard_layout.addWidget(self.catLabel)
        self.catCard_layout.addWidget(self.catimg)

    def init_adminCategoryCard(self) :
        # has edit/del btns , edit/trash icons in the card
        self.init_customerCategoryCard()
        self.editBtn = QPushButton("edit")
        self.editBtn.clicked.connect(self.editCatDialog.exec)
        self.catCard_layout.addWidget(self.editBtn)
        self.delBtn = QPushButton("delete")
        self.delBtn.clicked.connect(self.handleCatDelete)
        self.catCard_layout.addWidget(self.delBtn)

    def handleCatDelete(self) :
        deleteCategory(self.category_id)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.handleCatCardClicked()

    def handleCatCardClicked(self) :
        pubsub.publish(self.publishClickedEvent, (self.category_id, self.catname))
        # self.update_listContent(self.category_id, self.catname)
        self.stackedLists.setCurrentIndex(1)
    
