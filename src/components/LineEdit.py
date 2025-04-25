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
                                    QSecondaryButton,)
from src.components.SpinBox import QCartItemSpinBox
from src.components.Calendar import QCalendarFilter
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtCore import QEvent
from src.utils.PubSub import pubsub

class QSearchArea(QFrame) :
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.floatArea = QFloatArea()
        self.searchbar = QLineEdit(self)
        self.searchbar.textChanged.connect(self.floatArea.renderArea)
        self.searchbar.installEventFilter(self)
        self.searchbar.setFixedSize(300,30)

        self.main_layout.addWidget(self.searchbar)

        QTimer.singleShot(0, self.moveFloater_toPos)
        pubsub.subscribe("resize_event", self.moveFloater_toPos)
        self.floatArea.hide()

    def eventFilter(self, watched, event):
        if watched == self.searchbar:
            if event.type() == QEvent.Type.FocusIn:
                self.floatArea.show()
            elif event.type() == QEvent.Type.FocusOut:
                self.floatArea.hide()
        return super().eventFilter(watched, event)

    def moveFloater_toPos(self, e = None) :
        self.floatArea.setParent(self.window())
        globalpos = self.searchbar.mapToGlobal(QPoint(0, self.searchbar.height()))
        print(globalpos)
        self.floatArea.move(globalpos)
        self.floatArea.raise_()

class QFloatArea(QFrame) :
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")
        self.setFixedSize(300,200)
        # self.setFixedWidth(300)
        self.setMaximumHeight(0)
        self.main_layout = QVBoxLayout(self) # make layout to be scrollarea
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(QSearchRowItem())
        self.main_layout.addWidget(QSearchRowItem())
        self.main_layout.addWidget(QSearchRowItem())

    def renderArea(self, text) :
        #clear layout everytime
        print(text)
        # based on the text, get all items with matching text, only name: substr,
        # preferably with matching substr bold

        # get list

        # for loop list, render and create QSearchRowItem

    def clear_layout(self, layout): 
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   

class QSearchRowItem(QFrame) :
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,40)
        self.setStyleSheet("background-color:red")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Left button clicked!")
        return super().mousePressEvent(event)
    
        # if chosen card is category,

            # redirect to category panel,
                # ensure the category card is visible (autoscroll)
        
        # if chosen card is food,

            # updatecontent food panel
                # redirect to food panel
                    # ensure the food card is visible (autoscroll)

        # possible workarounds :
            # - each panel/list will have map of their cards, key of id, value of the obj

