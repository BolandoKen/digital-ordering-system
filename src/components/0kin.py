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
    QPushButton,
    QCalendarWidget,
    QDateEdit,
    QLabel,
    QListView,
    QLineEdit
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QShortcut, QKeySequence
from src.components.ComboBox import QFilterButton  
from src.components.Buttons import (QDeleteButton,
                                    QBackButton,
                                    QDineInButton,
                                    QTakeOutButton,
                                    QPlusButton,
                                    QMinusButton,
                                    QPrimaryButton,
                                    QSecondaryButton,
                                    QPreviousButton,)
from src.components.SpinBox import QCartItemSpinBox
from src.components.Calendar import QCalendarFilter
from PyQt6.QtCore import QDate, QTimer
from src.components.LineEdit import QSearchArea
from src.utils.PubSub import pubsub
class TestFrame(QFrame) :
    def __init__(self, floater = None):
        super().__init__()
        self.floater = floater
        print(self.window())
        self.floater = QLabel("hi")
        # QTimer.singleShot(0, lambda: self.floater.setParent(self.window()))
        main_layout = QHBoxLayout(self)
        self.lineedit = QLineEdit(self)
        self.lineedit.setFixedHeight(40)
        print(self.lineedit.pos().x(), self.lineedit.pos().y())
        globalpos = self.lineedit.mapToGlobal(QPoint(0,0))

        self.floater.setStyleSheet("background-color: red; color: white;")
        self.floater.setFixedSize(300,250)
        print(globalpos.x(), globalpos.y())
        main_layout.addWidget(self.lineedit)
        QTimer.singleShot(0, self.get_global_position)


    def get_global_position(self):
        # Now that the layout has been applied, get the global position
        xpos = self.lineedit.pos().x()
        ypos = self.lineedit.pos().y()
        self.floater.setParent(self.window())
        print(self.window())
        xoffset = 0
        yoffset = self.lineedit.height()
        globalpos = self.lineedit.mapToGlobal(QPoint(xoffset,yoffset))
        print("Global Position:", globalpos)
        self.floater.move(globalpos)
        self.floater.show()
        print(self.floater.pos().x(), self.floater.pos().y())
        # self.floater.move(globalpos)
        # self.floater.move(0,0)
        self.floater.raise_()


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)

        main_layout = QVBoxLayout()
        
        center_layout = QHBoxLayout()
        center_layout.addStretch() 
        print(self.window())
        self.filter_button = QFilterButton(self)
        center_layout.addWidget(self.filter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        center_layout.addStretch() 
        date_edit = QDateEdit()
        date_edit.setFixedWidth(100)
        date_edit.setCalendarPopup(True)  # enables the calendar popup
        date_edit.setDate(QDate.currentDate())

        delete_button = QDeleteButton()
        back_button = QBackButton()
        # logo_button = QLogoButton("assets/icons/Logo.png", "M'sKitchen")
        dineIn_button = QDineInButton()
        takeOut_button = QTakeOutButton()
        plus_button = QPlusButton()
        minus_button = QMinusButton()
        primbotn = QPrimaryButton("hi primary", 400)
        btn = QPushButton("al;dksfj;laj")
        # main_layout.addWidget(date_edit)
        # main_layout.addLayout(center_layout)
        # main_layout.addSpacing(20)
        # main_layout.addWidget(QCalendarFilter(), alignment=Qt.AlignmentFlag.AlignCenter)
        # main_layout.addWidget(delete_button)
        # main_layout.addWidget(back_button)
        # # main_layout.addWidget(logo_button)
        # # main_layout.addWidget(dineIn_button)
        # # main_layout.addWidget(takeOut_button)
        # main_layout.addWidget(plus_button)
        # main_layout.addWidget(minus_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # main_layout.addWidget(btn)
        # main_layout.addWidget(primbotn)
        # main_layout.addWidget(QSecondaryButton("hi secondary", 400))
        # main_layout.addWidget(QCartItemSpinBox())
        # self.floater = QLabel("hi", self.window())

        # testframe = TestFrame(self.floater)
        # testframe = TestFrame()
        # main_layout.addWidget(testframe)
        main_layout.addWidget(QSearchArea())
        
        main_centralwidget = QWidget()
        main_centralwidget.setStyleSheet("background: white; color: black")
        main_centralwidget.setLayout(main_layout)
        self.setCentralWidget(main_centralwidget)

        exit_shortcut = QShortcut(QKeySequence('esc'), self)
        exit_shortcut.activated.connect(self.close)

        # self.floater.raise_()
        # testframe.floater.raise_()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        pubsub.publish("resize_event")

if __name__ == "__main__":
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())