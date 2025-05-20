import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog,
    QSizePolicy,
    QRadioButton
)
from PyQt6.QtWidgets import QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QMouseEvent, QFont
from PyQt6.QtCore import Qt
from src.components.MenuCards import QMenuCard
from src.utils.PixMap import setPixMapOf
from src.database.queries import ProfileQueries
from src.utils.PubSub import pubsub

class QDeleteButton(QPushButton):

    def __init__(self, state=None):
        super().__init__("")
        self.setFixedSize(25, 25)
       
        self.setStyleSheet("""
            background: transparent;
            border: none;
            padding: 0px;      
        """)
        
        self.setIcon(QIcon("assets/icons/delete_icon.svg"))
        self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("delete")
        if state == "confirm" :
            self.setIcon(QIcon("assets/icons/delete_icon2.svg"))

    
    def setState(self, state) :
        if state == "delete" :
            self.setIcon(QIcon("assets/icons/delete_icon.svg"))
            self.setToolTip("delete")
        elif state == "unavailable" :
            self.setIcon(QIcon("assets/icons/unavailable_icon.svg"))
            self.setToolTip("set unavailable")
        elif state == "revive" :
            self.setIcon(QIcon("assets/icons/revive_icon.svg"))
            self.setToolTip("revive")

class QBackButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(44, 44)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QEditButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(30, 30)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border: none;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/edit_icon.svg"))
        self.setIconSize(QSize(25, 25))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("edit")

class QEyeButton(QPushButton) :
    def __init__(self):
        super().__init__("")
        self.setFixedSize(44, 44)

        self.setStyleSheet("""
            background: transparent;
            background-color: white;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            padding: 0px;                 
        """)
        
        self.setIcon(QIcon("assets/icons/closedeye_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def setState(self, state) :
        if state == "hide" :
            self.setIcon(QIcon("assets/icons/eye_icon.svg"))
        elif state == "show" :
            self.setIcon(QIcon("assets/icons/closedeye_icon.svg"))


class QAddButton(QMenuCard) :
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel()
        setPixMapOf(label, "addCircle.svg", "icon")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()

class QAddFoodButton(QMenuCard) :
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel()
        self.setFixedSize(270, 380)
        setPixMapOf(label, "addCircle.svg", "icon")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def connectTo(self, callback) :
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()

class QPrimaryButton(QPushButton) :
    def __init__(self, text, width=None, height=None, fontSize=None, extra_style=""): 
        super().__init__(text)
        styleString = """
            background: #C8161D;
            border-radius: 10px;
            color: white;
            font-style: "Helvetica";
            font-weight: bold;
            padding: 5px;
            """ + extra_style
        if width is not None :
            self.setFixedWidth(width)
        if height is not None :
            self.setFixedHeight(height)
        if fontSize is not None :
            styleString += f"font-size: {fontSize}px;"
        self.setStyleSheet(styleString)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QSecondaryButton(QPushButton) :
    def __init__(self, text, width=None, height=None, fontSize=None): 
        super().__init__(text)
        styleString = """
            background: transparent;
            border-radius: 10px;
            border: 2px solid #D9D9D9;
            color: #C8161D;
            font-style: "Helvetica";
            font-weight: bold;
            padding: 5px;
        """
        if width is not None :
            self.setFixedWidth(width)
        if height is not None :
            self.setFixedHeight(height)
        if fontSize is not None :
            styleString += f"font-size: {fontSize}px;"
        self.setStyleSheet(styleString)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QTertiaryButton(QPushButton) :
    def __init__(self, text, width=None, height=None, fontSize=None): 
        super().__init__(text)
        styleString = """
            background: #FFCA40;
            border-radius: 10px;
            border: none;
            color: white;
            font-style: "Helvetica";
            font-weight: bold;
            padding: 5px;
        """
        if width is not None :
            self.setFixedWidth(width)
        if height is not None :
            self.setFixedHeight(height)
        if fontSize is not None :
            styleString += f"font-size: {fontSize}px;"
        self.setStyleSheet(styleString)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QQuaternaryButton(QPushButton) :
    def __init__(self, text, width=None, height=None, fontSize=None): 
        super().__init__(text)
        styleString = """
            background: transparent;
            border-radius: 10px;
            border: 2px solid white;
            color: white;
            font-style: "Helvetica";
            font-weight: bold;
            padding: 5px;
        """
        if width is not None :
            self.setFixedWidth(width)
        if height is not None :
            self.setFixedHeight(height)
        if fontSize is not None :
            styleString += f"font-size: {fontSize}px;"
        self.setStyleSheet(styleString)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QDineInButton(QPushButton):
    def __init__(self, width=400, height=400):
        super().__init__("")
        self.setFixedSize(width, height)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)

        icon_label = QLabel() 
        icon_path = "assets/icons/dineIn_icon.svg"  
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(239, 200)))
        icon_label.setStyleSheet("background: transparent;") 
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        text_label = QLabel("Dine In") 
        text_label.setFont(QFont("Helvetica", 60, QFont.Weight.Bold))
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("background: transparent; color: black;")
        layout.addWidget(text_label)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFCA40;
                border-radius: 10px;
                padding-top: 120px;
            }
        """)


class QTakeOutButton(QPushButton):
    def __init__(self, width=400, height=400):
        super().__init__("")
        self.setFixedSize(width, height)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)

        icon_label = QLabel() 
        icon_path = "assets/icons/takeOut_icon.svg"  
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(239, 200)))
        icon_label.setStyleSheet("background: transparent;") 
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        text_label = QLabel("Take Out") 
        text_label.setFont(QFont("Helvetica", 60, QFont.Weight.Bold))
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("background: transparent; color: white;")
        layout.addWidget(text_label)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 10px;
                border: 4px solid white;
                padding-top: 120px;
            }
        """)

class QPlusButton(QPushButton):
    def __init__(self, width = 80, height = 60):
        super().__init__("")
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            background: #FFCA40;
            border: none;
            border-radius: 10px;
            padding: 0px;      
        """)
        
        self.setIcon(QIcon("assets/icons/plus_icon.svg"))
        self.setIconSize(QSize(15, 15))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QMinusButton(QPushButton):
    def __init__(self, width = 80, height = 60):
        super().__init__("")
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            background: transparent;
            border: 2px solid #D9D9D9;
            border-radius: 10px;
            padding: 0px;      
        """)
        
        self.setIcon(QIcon("assets/icons/minus_icon.svg"))
        self.setIconSize(QSize(15, 15))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class QAdminButton(QPushButton):
    def __init__(self, text, extra_style=""):
        super().__init__(text)

        self.styleString = """
            background-color: white;
            color: black;
            font-style: "Helvetica";
            font-size: 30px;
            font-weight: 450;
            padding: 10px;
            text-align: left;
            border: 2px solid #D9D9D9;
            """ +  extra_style
        self.setStyleSheet(self.styleString)

    def setClickedState(self, bool) :
        styleString = self.styleString
        if bool :
            styleString += "background-color:#D9D9D9;"
        self.setStyleSheet(styleString)

class QPreviousButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(32, 32)

        self.setStyleSheet("""
            background-color: white;
            padding: 0px;      
            border: none;          
           
        """)
        
        self.setIcon(QIcon("assets/icons/previous_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QNextButton(QPushButton):
    def __init__(self):
        super().__init__("")
        self.setFixedSize(32, 32)

        self.setStyleSheet("""
            background-color: white;
            padding: 0px;       
            border: none;          
        """)
        
        self.setIcon(QIcon("assets/icons/next_icon.svg"))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QCloseButton(QPushButton) :
    def __init__(self) :
        super().__init__()

        self.setStyleSheet("""
            background-color: transparent;
            padding: 0px;       
            border: none;          
        """)
        self.setIcon(QIcon("assets/icons/x_icon.svg"))
        self.setIconSize(QSize(16, 16))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class QOrderDetailsButton(QPushButton) :
    def __init__(self,) :
        super().__init__()
        self.setStyleSheet("""
            background-color: white; 
            padding: 5px;      
            border: none;
        """)
        self.setIcon(QIcon("assets/icons/orderDetails_icon.svg"))
        self.setIconSize(QSize(12, 2))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
class QProfileRadioButton(QRadioButton) :
    def __init__(self, text, parent = None) :
        super().__init__(text, parent)
        self.init_checked()
        pubsub.subscribe("updateProfile", self.init_checked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def init_checked(self, e=None) :
        self.is_displayname69 = ProfileQueries.fetchDisplayName()
        self.setChecked(self.is_displayname69)


class QBongoBtn(QPushButton):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setFixedSize(80, 80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self)
        self.label.setStyleSheet("background: transparent;")
        self.label.setFixedSize(80, 80)

        self.movie = QMovie("assets/icons/bongo_loading_tp3.gif")
        self.movie.setScaledSize(QSize(80, 80))
        self.label.setMovie(self.movie)
        self.movie.start()
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.label)
    
    def setState(self, state) :
        if state == "offline" :
            self.movie.stop()
            setPixMapOf(self.label, "bongo_tp.png", "icon")
            self.label.setScaledContents(True)
            self.label.setFixedSize(80, 80)

        elif state == "online" :
            self.movie.stop()
            setPixMapOf(self.label, "bongo_blue_tp.png", "icon")
            self.label.setScaledContents(True)
            self.label.setFixedSize(80, 80)

        elif state == "loading" :
            self.label.setMovie(self.movie)
            self.movie.start()

class QMostOrderedWidgetButton(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ascending = True
        self.setFixedWidth(280)
        self.text_label = QLabel("Most Ordered")
        self.icon_label = QPushButton()
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.icon_label.setStyleSheet("border: none; background: transparent;")
        #self.icon_label.setFixedSize(QSize(29, 29))
        self.asc_icon = QIcon("assets/icons/Ascending_Icon.svg")

        self.desc_icon = QIcon("assets/icons/Descending_Icon.svg")
        self.icon_label.setIconSize(QSize(29,29))

        self.icon_label.setIcon(self.asc_icon)
        # self.icon_label.setStyleSheet("padding: 10px")

        layout = QHBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.icon_label)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                font-family: "Helvetica";
                font-size: 30px;
                background: transparent; 
                padding: 5px;
            }
            QFrame:hover {
                background-color: #D9D9D9;
                border-radius: 10px;
            }
        """)
        self.cb = None

    def mousePressEvent(self, event):
        self.toggle_icon()
        if self.cb is not None :
            self.cb()

    def clicked_connect(self, cb) :
        self.cb = cb

    def toggle_icon(self):
        self.ascending = not self.ascending
        new_icon = self.asc_icon if self.ascending else self.desc_icon
        new_text = "Most Ordered" if self.ascending else "Least Ordered"
        self.text_label.setText(new_text)
        self.icon_label.setIcon(new_icon)