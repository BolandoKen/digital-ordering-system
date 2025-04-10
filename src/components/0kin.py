import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QFrame,
)
from Buttons import QButton1
from CatStatus import QStatusIndicator

class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout Example")
        main_layout = QVBoxLayout()

        main_layout.addWidget(QButton1("hello",100,50,"white","red"))
        main_layout.addWidget(QStatusIndicator(1,2))
        main_centralwidget = QWidget()
        main_centralwidget.setStyleSheet("background")
        main_centralwidget.setLayout(main_layout)
        self.setCentralWidget(main_centralwidget)
        


if __name__ == "__main__":
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())