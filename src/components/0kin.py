import sys
import os
sys.path.append(os.path.abspath("."))
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFrame,
    QDialog,
    QGraphicsDropShadowEffect,
    QPushButton

)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from src.components.ComboBox import QFilterButton  
from src.components.Buttons import (QDeleteButton,
                                    QBackButton,
                                    QDineInButton,
                                    QTakeOutButton,
                                    QPlusButton,
                                    QMinusButton,
                                    QPrimaryButton,
                                    QSecondaryButton,)
from src.components.SpinBox import QCartItemSpinBox

class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)

        main_layout = QVBoxLayout()
        
        center_layout = QHBoxLayout()
        center_layout.addStretch() 
        
        self.filter_button = QFilterButton(self)
        center_layout.addWidget(self.filter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        center_layout.addStretch() 
        
        main_layout.addLayout(center_layout)
        main_layout.addSpacing(20)
        delete_button = QDeleteButton()
        back_button = QBackButton()
        # logo_button = QLogoButton("assets/icons/Logo.png", "M'sKitchen")
        dineIn_button = QDineInButton()
        takeOut_button = QTakeOutButton()
        plus_button = QPlusButton()
        minus_button = QMinusButton()
        primbotn = QPrimaryButton("hi primary", 400)
        btn = QPushButton("al;dksfj;laj")

        main_layout.addWidget(delete_button)
        main_layout.addWidget(back_button)
        # main_layout.addWidget(logo_button)
        # main_layout.addWidget(dineIn_button)
        # main_layout.addWidget(takeOut_button)
        main_layout.addWidget(plus_button)
        main_layout.addWidget(minus_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(btn)
        main_layout.addWidget(primbotn)
        main_layout.addWidget(QSecondaryButton("hi secondary", 400))
        main_layout.addWidget(QCartItemSpinBox())

        
        main_centralwidget = QWidget()
        main_centralwidget.setStyleSheet("background: white; color: black")
        main_centralwidget.setLayout(main_layout)
        self.setCentralWidget(main_centralwidget)

        exit_shortcut = QShortcut(QKeySequence('esc'), self)
        exit_shortcut.activated.connect(self.close)
    

if __name__ == "__main__":
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())