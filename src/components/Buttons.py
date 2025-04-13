import sys
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from src.components.MenuCards import QMenuCard
from src.utils.PixMap import setPixMapOf

class QButton1(QPushButton) :
    def __init__(self, text, width, height, color, text_color, icon=None, font_style="Regular", font_size=20):
        super().__init__(text if text else "")
        self.setFixedSize(width, height)
        self.setStyleSheet(f"""
                           background-color: {color};
                           color: {text_color};
                           border-radius: 10px;
                           font-family: 'Helvietica';
                           font-size: {font_size}px;
                           font-weight: {font_style};
                           """)
        self.clicked.connect(self.on_click)
        if icon: # if an icon is provided
            self.setIcon(QIcon(icon))
            self.setIconSize(self.size())

    def on_click(self):
        print(f"Button clicked: {self.text()}")

class QImageButton(QLabel) :
    def __init__(self, text) :
        super().__init__(text)
    
    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()


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