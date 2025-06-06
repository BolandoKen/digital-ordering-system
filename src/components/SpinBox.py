from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLineEdit,
)
from src.components.Buttons import QPlusButton, QMinusButton
from PyQt6.QtGui import QFont, QIntValidator,  QIcon
from PyQt6.QtCore import Qt

# spinbox for pagenav
# spinbox for fooditem cart incrementer

class QCartItemSpinBox(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self) 
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setSpacing(20)
        self.plusBtn = QPlusButton(48,30)
        self.plusBtn.clicked.connect(self.handlePlusClicked)

        self.minusBtn = QMinusButton(48,30)
        self.minusBtn.clicked.connect(self.handleMinusClicked)
        self.quantityLineEdit = QLineEdit()
        # make custom lineedit for focusout events
        self.quantityLineEdit.setText("1")
        self.quantityLineEdit.setFixedWidth(40)
        self.quantityLineEdit.setFont(QFont("Helvetica", 20, QFont.Weight.Bold))
        self.quantityLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quantityLineEdit.setStyleSheet("border:none;")
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
        #publish here, noo, i said no pubsub in temp objects!
    
    def handlePlusClicked(self) :
        if self.quantity == 99 :
            return
        self.quantity += 1 
        self.quantityLineEdit.setText(str(self.quantity))
        
        #publish here
    def setQuantity(self, quantity) :
        self.quantity = int(quantity)
        self.quantityLineEdit.setText(str(self.quantity))
    
    def connectOnChangeTo(self, cb) :
        self.quantityLineEdit.textChanged.connect(lambda: self.handleLineEditChanged(cb))
    
    def handleLineEditChanged(self, cb) :
            
        if self.quantityLineEdit.text() == '' :
            return
        if self.quantityLineEdit.text() == "0" :
            self.quantityLineEdit.setText("1")
        self.quantityLineEdit.setText(str(int(self.quantityLineEdit.text())))
        self.quantity = int(self.quantityLineEdit.text())
        cb()
    
    def setState(self, state) :
        if state == "cart" :
            self.plusBtn.setIcon(QIcon("assets/icons/plus_icon.svg"))
            self.minusBtn.setIcon(QIcon("assets/icons/minus_icon.svg"))
            self.minusBtn.setStyleSheet("""
            background: transparent;
            border: 2px solid black;
            border-radius: 10px;
            padding: 0px;      
        """)
        elif state == "confirm" :
            self.plusBtn.setIcon(QIcon("assets/icons/plus_icon2.svg"))
            self.minusBtn.setIcon(QIcon("assets/icons/minus_icon2.svg"))
            self.minusBtn.setStyleSheet("""
            background: transparent;
            border: 2px solid white;
            border-radius: 10px;
            padding: 0px;      
        """)



    def getQuantity(self) :
        return self.quantity

