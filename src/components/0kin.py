import sys
import os
sys.path.append(os.path.abspath("."))
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from src.components.ComboBox import QFilterButton  

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