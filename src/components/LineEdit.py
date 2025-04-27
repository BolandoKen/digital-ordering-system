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
    QLineEdit,
    QGraphicsDropShadowEffect

)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QShortcut, QKeySequence, QColor
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
from src.database.queries import fetchSubStrNames
from src.components.ScrollArea import QScrollAreaLayout

class QSearchArea(QFrame) :
    def __init__(self, parent = None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.floatArea = QFloatArea()
        self.searchbar = QLineEdit(self)
        self.setFixedHeight(40)
        self.searchbar.textChanged.connect(self.floatArea.renderArea)
        self.searchbar.installEventFilter(self)
        self.searchbar.setFixedSize(450,30)
        self.temp = [0]
        self.main_layout.addWidget(self.searchbar, Qt.AlignmentFlag.AlignRight)

        QTimer.singleShot(0, self.moveFloater_toPos)
        pubsub.subscribe("resize_event", self.moveFloater_toPos)
        self.floatArea.hide()
        self.searchbar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        pubsub.subscribe("foodSearched_event", self.set_searchbarText)

    def eventFilter(self, watched, event):
        if watched == self.searchbar:
            if event.type() == QEvent.Type.FocusIn:
                self.moveFloater_toPos()
                self.floatArea.show()
            elif event.type() == QEvent.Type.FocusOut:
                self.floatArea.hide()
        return super().eventFilter(watched, event)

    def moveFloater_toPos(self, e = None) :
        self.floatArea.setParent(self.window())
        globalpos = self.searchbar.mapToGlobal(QPoint(0, self.searchbar.height()))
        self.floatArea.move(globalpos)
        self.floatArea.raise_()

    def set_searchbarText(self, tuple) :
        foodname = tuple[1]
        self.searchbar.setText(foodname)


class QFloatArea(QFrame) :
    def __init__(self):
        super().__init__()
        self.setObjectName("floatarea")
        self.setStyleSheet("""#floatarea{
                           background-color: white;
                            border: 1px solid #D9D9D9; 
                            border-radius: 10px;
                           padding:3px;}""")
        self.setFixedSize(450,100)
        # self.setFixedWidth(300)
        self.setMaximumHeight(0)
        self.mainmain_layout = QVBoxLayout(self)
        self.main_layout = QScrollAreaLayout(QVBoxLayout, self.mainmain_layout) # make layout to be scrollarea
        self.main_layout.myLayout.setContentsMargins(0,0,0,0)
        self.main_layout.myLayout.setSpacing(0)
        self.main_layout.myLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainmain_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.contentCount = 0
        self.setFixedHeight(0)
  
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

    def renderArea(self, text) :
        #clear layout everytime
        self.clear_layout(self.main_layout.getLayout())
        if text.strip() == "" : 
            self.contentCount = 0
            self.setFixedHeight(0)
            return
        listResults = fetchSubStrNames(text)
        self.contentCount = len(listResults)
        height = 100
        if self.contentCount == 0 :  # WHY IS SIZING NOT CONSISTENT? its impossible with min(formula, 100) >:(())
            height = 0 
        elif self.contentCount == 1 :
            height = 40 
        elif self.contentCount == 2 :
            height = 70
        
        self.setFixedHeight(height)
        
        for tuple in listResults :
            self.main_layout.addWidget(QSearchRowItem(tuple))
        

        # based on the text, get all items with matching text, only name: substr,
        # preferably with matching substr bold, no ty

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
    def __init__(self, rowTuple):
        super().__init__()
        self.rowTuple =rowTuple
        self.foodid , self.foodname, self.isavailable, self.catid, self.catname = rowTuple
        self.setFixedSize(400,30)
        self.setStyleSheet("background-color:white; border-radius:2px; ")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(QLabel(f"{self.foodname} - {self.catname}"))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Left button clicked!", self.foodname)
        pubsub.publish("foodSearched_event", self.rowTuple )
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

