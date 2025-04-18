from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
from src.components.Buttons import QPlusButton, QMinusButton
from PyQt6.QtGui import QPixmap, QMouseEvent, QFont, QIntValidator
from PyQt6.QtCore import Qt

# spinbox for pagenav
# spinbox for fooditem cart incrementer

class QCartItemSpinBox(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self) 
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setSpacing(20)
        self.plusBtn = QPlusButton()
        self.plusBtn.clicked.connect(self.handlePlusClicked)

        self.minusBtn = QMinusButton()
        self.minusBtn.clicked.connect(self.handleMinusClicked)
        self.quantityLineEdit = QLineEdit()
        self.quantityLineEdit.setText("1")
        self.quantityLineEdit.setFixedWidth(70)
        self.quantityLineEdit.setFont(QFont("Helvetica", 27, QFont.Weight.Bold))
        self.quantityLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quantityLineEdit.setStyleSheet("border:none; border-bottom: 1px solid black;")
        self.quantityLineEdit.setValidator(QIntValidator(1, 99))
        self.quantity = 1
        self.main_layout.addWidget(self.minusBtn)
        self.main_layout.addWidget(self.quantityLineEdit)
        self.main_layout.addWidget(self.plusBtn)
    
    def handleMinusClicked(self) :
        if self.quantity == 1 :
            return
        self.quantity -= 1
        self.quantityLineEdit.setText(str(self.quantity))
    
    def handlePlusClicked(self) :
        self.quantity += 1 
        self.quantityLineEdit.setText(str(self.quantity))

    def getQuantity(self) :
        return self.quantity

