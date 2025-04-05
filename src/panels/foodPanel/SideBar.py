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


class QSideBar(QFrame) :
    def __init__(self, pageName) :
        super().__init__()
        self.pageName = pageName
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: white; color: black")

        if self.pageName == "admin" :
            self.init_adminSideBar()
        elif self.pageName == "customer" :
            self.init_customerSideBar()

    
    def init_customerSideBar(self) :
        self.sidebar_layout = QVBoxLayout(self)
        self.sidebar_layout.addStretch()
        self.submitBtn = QPushButton("SubmitBtn")
        self.submitBtn.clicked.connect(self.handleSubmitOrderClicked)
        self.sidebar_layout.addWidget(self.submitBtn)
    
    def init_adminSideBar(self) :
        print('adminSidebar')
    
    def handleSubmitOrderClicked(self) :
        print('will order, printing receipt')

    def handleFoodAddToCart(self, fooditem_id, foodname) :
        print(fooditem_id,foodname, "added to cart")