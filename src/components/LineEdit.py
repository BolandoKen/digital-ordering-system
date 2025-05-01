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
    QGraphicsDropShadowEffect,
    QSpacerItem

)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QShortcut, QKeySequence, QColor, QIcon, QKeyEvent
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
from src.utils.PixMap import setPixMapOf
from src.database.queries import fetchSubStrNames, ProfileQueries
from src.components.ScrollArea import QScrollAreaLayout

class QSearchArea(QFrame) :
    def __init__(self, parent = None, typeOf = None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.floatArea = QFloatArea()
        self.searchbar = QLineEdit(self)
        self.styleStr = """
                background-color: white; 
                border: 2px solid #D9D9D9; 
                border-radius: 10px;
                outline: none;
                padding: 2px;                
            """
        self.setObjectName("searcharea")
        self.setStyleSheet("#searcharea{margin-bottom:5px; }")
        self.searchbar.setStyleSheet(self.styleStr)
        self.setFixedHeight(50)
        self.searchbar.textChanged.connect(self.floatArea.renderArea)
        self.searchbar.setFixedSize(450,30)
        self.temp = [0]
        searchIcon = QPushButton() 
        searchIcon.setIcon(QIcon("assets/icons/Search.svg"))
        searchIcon.setFixedSize(32,32)
        searchIcon.setStyleSheet("background:transparent; border: none;")
        searchIcon.setIconSize(QSize(30,30))
        self.main_layout.addWidget(searchIcon, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addWidget(self.searchbar)
        self.main_layout.addStretch()
        if typeOf != "stats" :
            self.searchbar.installEventFilter(self)
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
        parenwindow = self.window()
        self.floatArea.setParent(self.window())
        globalpos = self.searchbar.mapToGlobal(QPoint(0, self.searchbar.height()))
        relativepos = parenwindow.mapFromGlobal(globalpos)
        self.floatArea.move(relativepos)
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


class QStyledLineEdit(QLineEdit) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.setFixedSize(300,30)
        self.styleStr = """
                background-color: white; 
                border: 2px solid #D9D9D9; 
                border-radius: 10px;
                outline: none;
                padding: 2px;                
            """
        self.setStyleSheet(self.styleStr)


class QFormLineEdit(QLineEdit) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.setFixedSize(300,30)
        self.styleStr = """
                background-color: white; 
                border: 2px solid #D9D9D9; 
                border-radius: 10px;
                outline: none;
                padding: 2px;                
            """
        self.setStyleSheet(self.styleStr)
        self.mypopup = QLineEditPopup()
        # QTimer.singleShot(100, self.setState)
        # self.setStateInvalid("necessary field!")
        # self.installEventFilter(self)
        # self.setStateInvalid()
        self.textChanged.connect(self.setStateInit)

    def eventFilter(self, watched, event):
        if watched == self:
            if event.type() == QEvent.Type.FocusIn:
                self.setStateInit()
        return super().eventFilter(watched, event)

    def moveFloater_toPos(self, typeOf = None) :
        parenwindow = self.window()
        self.mypopup.setParent(self.window())
        print(self.width(), self.height())
        globalpos = self.mapToGlobal(QPoint(self.width() - self.mypopup.width() - 10, 0 - self.mypopup.height()))
        relativepos = parenwindow.mapFromGlobal(globalpos)
        self.mypopup.move(relativepos)
        self.mypopup.raise_()
        if typeOf == "valid" :
            self.mypopup.hide() 
        else :
            self.mypopup.show()
    
    def setStateInvalid(self, text) :
        if text is None : 
            return
        invalidstyle = self.styleStr + "border:2px solid red;"
        self.setStyleSheet(invalidstyle)
        self.mypopup.setText(text)
        self.mypopup.adjustSize()
        QTimer.singleShot(100, self.moveFloater_toPos)
    
    def setStateInit(self) :
        self.setStyleSheet(self.styleStr)
        self.mypopup.hide()


class QLineEditPopup (QLabel) :
    def __init__(self) :
        super().__init__()
        # self.setFixedSize(150,30)
        self.setFixedHeight(30)
        self.setText("Warning, invalid")
        self.setStyleSheet("background-color:red; border-top-left-radius: 10px; border-top-right-radius: 10px; padding:3px; color:white")

class QProfileLineEdit(QFormLineEdit) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.setFixedSize(250,50)
        self.init_text()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def init_text(self) :
        self.setText(ProfileQueries.fetchProfileName())


class QPinInputBox(QFrame) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.test = None

        self.main_layout = QHBoxLayout(self) 
        self.charBoxArr = [QCharacterBox(self), QCharacterBox(self), QCharacterBox(self), QCharacterBox(self)]
        for i in range(len(self.charBoxArr)) :
            self.main_layout.addWidget(self.charBoxArr[i])

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.installEventFilter(self)
        self.curr = 0 
        self.charBoxArr[0].setState_curr(True)
        self.cb = None

    def eventFilter(self, watched, event) :
        if watched == self:
            if event.type() == QEvent.Type.FocusIn:
                self.updateChildrenStates()
            elif event.type() == QEvent.Type.FocusOut:
                self.updateChildrenStates()
            
            if event.type() == QEvent.Type.KeyPress :
                text = event.text()
                if text.isdigit() :
                    if self.curr == len(self.charBoxArr):
                        # print(self.curr)
                        return super().eventFilter(watched, event)
                    self.charBoxArr[self.curr].setChar(text)
                    self.curr += 1
                    self.updateChildrenStates()
                elif event.key() == Qt.Key.Key_Backspace :
                    if self.curr == 0 :
                        return super().eventFilter(watched, event)
                    self.curr -= 1
                    self.charBoxArr[self.curr].setChar("")
                    self.updateChildrenStates()
                    # print('backspace')

        return super().eventFilter(watched, event)

    def updateChildrenStates(self) :
        for i in range(len(self.charBoxArr)) :
            box = self.charBoxArr[i]
            box.setState_curr(i == self.curr)

        if self.cb is not None :
            self.cb()
    
    def text(self) :
        return "".join([box.character for box in self.charBoxArr])

    def onChange_connectTo(self, cb) :
        self.cb = cb
     
    def clearText(self) :
        self.curr = 0 
        for i in range(len(self.charBoxArr)) :
            box = self.charBoxArr[i]
            box.setChar("")
            box.setState_curr(i == self.curr)


class QCharacterBox(QLabel) :
    def __init__(self, parent = None) :
        super().__init__(parent)   
        self.parent = parent
        self.state_isCurr = False
        self.character = ''
        self.updateState()

    
    def setChar(self, char) :
        self.character = char
    
    def setState_curr(self, iscurr) :
        self.state_isCurr = iscurr
        self.updateState()
    
    def updateState(self) :
        parenthasFocus = self.parent.hasFocus()
        self.focusedState = "" if parenthasFocus else "Unfocused"
        if self.character != '' :
            self.setSelfPixmap(f"numberboxFilled{self.focusedState}_icon.svg")
        elif self.state_isCurr and self.character == '' and parenthasFocus:
            self.setSelfPixmap("numberboxCurr_icon.svg")
        else :
            self.setSelfPixmap(f"numberboxEmpty{self.focusedState}_icon.svg")
        
    def setSelfPixmap(self, stateIcon) :
        setPixMapOf(self, stateIcon, "icon")
        self.setScaledContents(True)
        self.setFixedSize(50,50)
