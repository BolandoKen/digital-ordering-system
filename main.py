import sys
import atexit
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
import asyncio
from PyQt6.QtGui import QShortcut, QKeySequence
from qasync import QEventLoop, asyncSlot
from src.pages.AdminPage import QAdminPage
from src.pages.CustomerPage import QCustomerPage
from src.database.init_db import init_db
from src.utils.PubSub import pubsub
from src.utils.CatPrinter.CatPrinter import CatPrinter
from PyQt6.QtWidgets import QStyleFactory


class QWindow(QMainWindow) :
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Orderoo")
        self.setGeometry(0,0,900,700)
        self.setStyleSheet("background-color: white; color: black")

        self.stackedPages = QStackedWidget()
        self.CustomerPage = QCustomerPage()
        self.AdminPage = QAdminPage()

        self.catPrinter = CatPrinter()

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
        pubsub.subscribe("print_event", self.intitiate_catPrint)
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

    @asyncSlot()
    async def intitiate_catPrint(self, myOrder = None) :   
        await self.catPrinter.print_sequence(myOrder)


    def resizeEvent(self, event):
        super().resizeEvent(event)





async def main() :
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = QWindow()
    window.show()


    with loop:
        try :
            loop.run_forever()
        finally :
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            loop.run_until_complete(window.catPrinter.disconnect_catPrinter())
        
if __name__ == "__main__" :
    asyncio.run(main())
