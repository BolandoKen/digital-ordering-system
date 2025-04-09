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
from PyQt6.QtCore import Qt


class QButton1(QPushButton) :
    def __init__(self, text) :
        super().__init__(text)
        self.setStyleSheet("background-color: black; color: white")
    

class QImageButton(QLabel) :
    def __init__(self, text) :
        super().__init__(text)
    
    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()


