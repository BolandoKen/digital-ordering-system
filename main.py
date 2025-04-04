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
from PyQt6.QtGui import QShortcut, QKeySequence
from src.pages.AdminPage import QAdminPage
from src.pages.CustomerPage import QCustomerPage

class QWindow(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setWindowTitle("digimon system")
        self.setGeometry(0,0,800,500)

        self.stackedPages = QStackedWidget()
        self.CustomerPage = QCustomerPage()
        self.AdminPage = QAdminPage()

        self.stackedPages.addWidget(self.CustomerPage)
        self.stackedPages.addWidget(self.AdminPage)

        self.switchBtn = QPushButton("switch")
        self.switchBtn.clicked.connect(self.switchPage)

        centralWidget = QWidget()
        main_layout = QVBoxLayout(centralWidget)
        main_layout.addWidget(self.stackedPages)
        main_layout.addWidget(self.switchBtn)
        self.setCentralWidget(centralWidget)

        exit_shortcut = QShortcut(QKeySequence('esc'), self)
        exit_shortcut.activated.connect(self.close)

    def switchPage(self) :
        curr = self.stackedPages.currentIndex()
        self.stackedPages.setCurrentIndex( (curr+1) %2)

if __name__ == "__main__" :
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())