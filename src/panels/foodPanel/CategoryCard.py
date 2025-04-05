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
)

class QCategoryCard(QPushButton) : # at the mean time make it a QPushBtn for simplicity
    # card for each category, display name
    def __init__(self, text, pageName) :
        super().__init__(text)
        self.pageName = pageName
        self.catCard_layout = QVBoxLayout(self)

    def init_customerCategoryCard(self) :
        self.setText(self.text()) # do nothing
        # no edit/del btns

    def init_adminCategoryCard(self) :
        self.setText(self.text() + "  edit/del btns")
        # has edit/del btns , edit/trash icons in the card