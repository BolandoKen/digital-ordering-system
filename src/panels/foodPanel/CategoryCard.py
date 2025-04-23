import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QMessageBox,
)
from src.utils.PubSub import pubsub
from src.database.Categories import deleteCategory
from src.components.Dialogs import QeditDialog, QConfirmDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from src.utils.PixMap import setPixMapOf
from src.components.MenuCards import QMenuCard
from src.database.queries import fetchCategoryAvailableItemCount, fetchCategoryUnavailableItemCount
from src.components.CatStatus import QCatStatusEditLayout, QStatusIndicator
from src.components.ImageCard import QCatLabelImageLayout
from src.components.Buttons import QDeleteButton, QEditButton
class QCategoryCard(QMenuCard) :
    def __init__(self, catTuple, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.category_id, self.catname, self.imgfile = catTuple
        self.availableItemCount = fetchCategoryAvailableItemCount(self.category_id) # will show only in admin
        self.unavailableItemCount = fetchCategoryUnavailableItemCount(self.category_id)
        self.editCatDialog = QeditDialog("category", catTuple, self.window())
        self.stackedLists = stackedLists
        self.catCard_layout = QVBoxLayout(self)
        self.catCard_layout.setSpacing(0)
        if self.pageName == "admin" :
            self.publishClickedEvent = "admin_catCardClicked"
            self.init_adminCategoryCard()
        elif self.pageName == "customer" :
            self.publishClickedEvent = "customer_catCardClicked"
            self.init_customerCategoryCard()


    def init_customerCategoryCard(self) :
        # no edit/del btns
        self.catLabelImg = QCatLabelImageLayout(self.catname, self.imgfile, "category")
        self.catCard_layout.addLayout(self.catLabelImg)

    def init_adminCategoryCard(self) :
        # has edit/del btns , edit/trash icons in the card
        self.init_customerCategoryCard()
        self.catCard_layout.addWidget(QStatusIndicator(self.availableItemCount, self.unavailableItemCount), alignment=Qt.AlignmentFlag.AlignLeft)
        # self.catCard_layout.addLayout(QCatStatusEditLayout(self.availableItemCount, self.unavailableItemCount, self.editCatDialog.exec))
        delHBoxLayout = QHBoxLayout()
        delHBoxLayout.setContentsMargins(0,0,0,0)
        delHBoxLayout.addStretch()
        self.editBtn = QEditButton() 
        self.editBtn.clicked.connect(self.editCatDialog.exec)
        self.delBtn = QDeleteButton()
        self.delBtn.clicked.connect(self.handleCatDelete)
        # delBtn_sizePolicy = self.delBtn.sizePolicy()
        # delBtn_sizePolicy.setRetainSizeWhenHidden(True)
        # self.delBtn.setSizePolicy(delBtn_sizePolicy)

        delHBoxLayout.addWidget(self.editBtn)
        delHBoxLayout.addWidget(self.delBtn)
 
        self.catCard_layout.insertLayout(0,delHBoxLayout)
        if self.availableItemCount > 0 or self.unavailableItemCount > 0:
            self.delBtn.hide()

    def handleCatDelete(self) :
        message = "Are you sure you want to delete this category?"
        confirm = QConfirmDialog("Confirm", message, self.window())

        if confirm.exec():
            deleteCategory(self.category_id) # published updateCategory was in the function
            pubsub.publish("updateCategory") 

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.handleCatCardClicked()

    def handleCatCardClicked(self) :
        pubsub.publish(self.publishClickedEvent, (self.category_id, self.catname))
        # self.update_listContent(self.category_id, self.catname)
        self.stackedLists.setCurrentIndex(1)
    
