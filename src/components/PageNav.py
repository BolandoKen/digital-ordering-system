from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFrame,
    )
from PyQt6.QtGui import QIntValidator, QCursor
from PyQt6.QtCore import Qt
from src.components.Buttons import QPreviousButton, QNextButton
import math

class QPageNav(QFrame) :
    def __init__(self, currentLastPage, renderPage) :
        super().__init__()
       
        self.renderPage = renderPage
        self.currentPage = 1
        self.currentLastPage = currentLastPage
        self.main_layout = QHBoxLayout()
        self.init_ui()
        self.setLayout(self.main_layout)

    def init_ui(self) :
        self.leftNav = QPreviousButton()
        self.rightNav = QNextButton()
        self.lineNav = QLineEdit(f"{self.currentPage}")

        self.leftNav.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.rightNav.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lineNav.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        left_sizepolicy = self.leftNav.sizePolicy()
        left_sizepolicy.setRetainSizeWhenHidden(True)
        right_sizepolicy = self.rightNav.sizePolicy()
        right_sizepolicy.setRetainSizeWhenHidden(True)
        line_sizepolicy = self.lineNav.sizePolicy()
        line_sizepolicy.setRetainSizeWhenHidden(True)

        self.leftNav.setSizePolicy(left_sizepolicy)
        self.rightNav.setSizePolicy(right_sizepolicy)
        self.lineNav.setSizePolicy(line_sizepolicy)

        self.leftNav.setShortcut(Qt.Key.Key_Left)
        self.rightNav.setShortcut(Qt.Key.Key_Right)

        self.lineNav.returnPressed.connect(lambda: self.handleNavClicked('line'))
        self.lineNav.setValidator(QIntValidator(0, 99999))
        self.leftNav.hide()
      
        self.lineNav.setStyleSheet("border: none;border-bottom: 0.5px solid #144272;")
        self.lineNav.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineNav.setFixedWidth(50)
        self.leftNav.setFixedWidth(50)
        self.rightNav.setFixedWidth(50)

        if self.currentPage == self.currentLastPage :
            self.rightNav.hide()
            self.lineNav.hide() # if on init, currlastpage is 1, hide them

        self.leftNav.clicked.connect(lambda: self.handleNavClicked('<'))
        self.rightNav.clicked.connect(lambda: self.handleNavClicked('>'))
        self.main_layout.addWidget(self.leftNav)
        self.main_layout.addWidget(self.lineNav)
        self.main_layout.addWidget(self.rightNav)

    def handleNavClicked(self, nav) :
        if (nav == '<') :
            self.currentPage -= 1
  
        elif (nav == '>') :
            self.currentPage += 1
        else:
            linePage = int(self.lineNav.text())
            if linePage <= 0 :
                self.currentPage = 1
            elif linePage > self.currentLastPage:
                self.currentPage = self.currentLastPage
            else :
                self.currentPage = linePage

        if self.currentPage == 1 :
     
            self.leftNav.hide()
        else :
            self.leftNav.show()
        if self.currentPage == self.currentLastPage :
            self.rightNav.hide()
        else :
            self.rightNav.show()
        
        self.lineNav.setText(f"{self.currentPage}")
        self.lineNav.clearFocus()
        self.renderPage()
    
    def updateNav(self, queriedArr, rows) :
        self.currentLastPage = max(1, math.ceil(len(queriedArr) / rows))
        self.currentPage = min(self.currentPage, self.currentLastPage)

        if self.currentLastPage > self.currentPage :
            self.lineNav.show()
            self.rightNav.show()
        elif self.currentLastPage == 1 :
            self.lineNav.setText(f"{self.currentPage}")
            self.leftNav.hide()
            self.rightNav.hide()
            self.lineNav.hide()
        else: # when currpage = curr last and is not 1
            self.lineNav.setText(f"{self.currentPage}")
            self.rightNav.hide()