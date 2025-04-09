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
from PyQt6.QtWidgets import QPushButton

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
       