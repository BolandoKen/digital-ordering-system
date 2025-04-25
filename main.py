import sys
# import os
# sys.path.append(os.path.abspath("src"))
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
from src.database.init_db import init_db
from src.utils.PubSub import pubsub

class QWindow(QMainWindow) :
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Orderoo")
        self.setGeometry(0,0,900,700)
        self.setStyleSheet("background-color: white; color: black")

        self.stackedPages = QStackedWidget()
        self.CustomerPage = QCustomerPage()
        self.AdminPage = QAdminPage()

        self.stackedPages.addWidget(self.CustomerPage)
        self.stackedPages.addWidget(self.AdminPage)

        self.switchBtn = QPushButton("login")
        self.switchBtn.clicked.connect(self.switchPage)

        centralWidget = QWidget()
        main_layout = QVBoxLayout(centralWidget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.stackedPages)
        self.setCentralWidget(centralWidget)

        pubsub.subscribe("login_Event", self.switchPage)
        pubsub.subscribe("logout_Event", self.switchPage)
        exit_shortcut = QShortcut(QKeySequence('esc'), self)
        exit_shortcut.activated.connect(self.close)

    def switchPage(self, e=None):
        curr = self.stackedPages.currentIndex()
        new_index = (curr + 1) % 2
        self.stackedPages.setCurrentIndex(new_index)
        if new_index == 0:
            self.switchBtn.setText("login")
            self.CustomerPage.customerFoodMenuPanel.sideBar.resetSidebar()
            self.CustomerPage.customerPage_stackedWidgets.setCurrentIndex(1)
            self.CustomerPage.customerFoodMenuPanel.foodPanel.menuListCont.switchToCatPanel()
        else:
            self.switchBtn.setText("logout")
            self.AdminPage.switchPage(0)


if __name__ == "__main__" :
    app = QApplication([])
    main_window = QWindow()
    init_db()
    main_window.show()

    sys.exit(app.exec())