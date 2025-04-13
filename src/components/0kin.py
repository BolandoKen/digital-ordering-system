import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFrame,
)
from PyQt6.QtCore import Qt
from Buttons import DeleteButton, BackButton, LogoButton

class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout Example")
        self.setFixedSize(1280, 720)

        main_layout = QVBoxLayout()
        delete_button = DeleteButton()
        back_button = BackButton()
        logo_button = LogoButton("assets/icons/Logo.png", "M'sKitchen")

        main_layout.addWidget(delete_button)
        main_layout.addWidget(back_button)
        main_layout.addWidget(logo_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_centralwidget = QWidget()
        main_centralwidget.setStyleSheet("background: white;")
        main_centralwidget.setLayout(main_layout)
        self.setCentralWidget(main_centralwidget)
        


if __name__ == "__main__":
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())