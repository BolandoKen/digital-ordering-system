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


class QButton1(QPushButton) :
    def __init__(self, text) :
        super().__init__(text)
        self.setStyleSheet("background-color: black; color: white")


