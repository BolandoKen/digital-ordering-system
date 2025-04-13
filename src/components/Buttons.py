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

class DeleteButton(QPushButton):

    def __init__(self):
        super().__init__("")
        self.setFixedSize(52, 52)
       
        self.setStyleSheet("""
            background: transparent;
            padding: 0px;                 
        """)
        
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon("assets/icons/delete_icon.svg"))
        self.setIconSize(QSize(32, 32))

    def on_click(self):
        print("Delete button clicked!")

class BackButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(44, 44)

        self.setStyleSheet("""
            background: transparent;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;                 
        """)
        
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.setIconSize(QSize(32, 32))

    def on_click(self):
        print("Back button clicked!")

class LogoButton(QWidget):
    def __init__(self, logo_path: str, eatery_name: str):
        super().__init__()
        self.setFixedSize(400, 70)
        self.setStyleSheet("""
            background: transparent;
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
        text_label.setFont(QFont("Helvitica", 30))
        layout.addWidget(text_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(layout)

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                print("Logo button clicked!")


class QAddButton(QMenuCard) : # not yet used
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