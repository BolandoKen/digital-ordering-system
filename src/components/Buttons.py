import sys
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
    QDialog,
    QLineEdit,
    QFileDialog,
    QSizePolicy
)
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QMouseEvent, QFont
from PyQt6.QtCore import Qt
from src.components.MenuCards import QMenuCard
from src.utils.PixMap import setPixMapOf

class QDeleteButton(QPushButton):

    def __init__(self):
        super().__init__("")
        self.setFixedSize(25, 25)
       
        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border: none;
            padding: 0px;      
        """)
        
        self.setIcon(QIcon("assets/icons/delete_icon.svg"))
        self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def setState(self, state) :
        if state == "delete" :
            self.setIcon(QIcon("assets/icons/delete_icon.svg"))
        elif state == "unavailable" :
            self.setIcon(QIcon("assets/icons/unavailable_icon.svg"))
        elif state == "revive" :
            self.setIcon(QIcon("assets/icons/revive_icon.svg"))

class QBackButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(44, 44)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QEditButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(30, 30)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border: none;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/edit_icon.svg"))
        self.setIconSize(QSize(25, 25))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QEyeButton(QPushButton) :
    def __init__(self):
        super().__init__("")
        self.setFixedSize(44, 44)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/closedeye_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def setState(self, state) :
        if state == "hide" :
            self.setIcon(QIcon("assets/icons/eye_icon.svg"))
        elif state == "show" :
            self.setIcon(QIcon("assets/icons/closedeye_icon.svg"))

class QLogoButton(QWidget):
    def __init__(self, logo_path: str, eatery_name: str, pageName):
        super().__init__()
        self.pageName = pageName
        self.setFixedSize(400, 70)
        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            padding: 0px;
            color: black;           
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0) 

        icon_label = QLabel()
        pixmap = QPixmap(logo_path).scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        text_label = QLabel(eatery_name)
        text_label.setFont(QFont("Helvitica", 15, QFont.Weight.Bold))
        layout.addWidget(text_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(layout)

    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if self.pageName == "admin" : return
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()


class QAddButton(QMenuCard) :
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel()
        setPixMapOf(label, "addCircle.svg", "icon")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()

class QImageButton(QLabel) :
    def __init__(self, text) :
        super().__init__(text)

    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()