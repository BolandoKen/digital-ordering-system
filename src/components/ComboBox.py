from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog,
    QComboBox
)
from src.database.queries import fetchCatList

import sys
from PyQt6.QtWidgets import QPushButton, QComboBox, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QIcon
 
class QPopupButton(QPushButton) : 
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(40, 40)
        

        self.setStyleSheet("""
            QPushButton{
                background: none;
                border: none;
                }
            QPushButton:hover{
                background: none;
                }
            QPushButton:pressed{
                background: none;
                }
        """)
        
        self.popup = QWidget(flags=Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.popup.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.popup.setObjectName("popup")
        self.popup.setStyleSheet("""
            #popup{background-color: white; 
            border: 2px solid #D9D9D9; 
            border-radius: 10px;
            outline: none;}
        """)

        self.container = QWidget(self.popup)
        self.popup.setFixedSize(193, 126)
        self.container.setGeometry(0, 0, 193, 126)
        self.container.setStyleSheet("""
            background-color: white; 
            border: 2px solid #D9D9D9; 
            border-radius: 10px;
        """)
        
        self.popup_layout = QVBoxLayout(self.popup)
        self.clicked.connect(self.toggle_popup)

    def toggle_popup(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            button_pos = self.mapToGlobal(QPoint(-152, self.height()))
            self.popup.move(button_pos)
            self.popup.show()

class QFilterButton(QPopupButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.popup.setFixedSize(193, 126)
        self.container.setGeometry(0, 0, 193, 126)
        category_label = QLabel("Category")
        category_label.setStyleSheet("""
                                     background-color: white;
                                     color: black;
                                     font-family: Helvetica;
                                     font-size: 20px; font-weight: regular;
                                     border: none;
                                     border-radius: 0px;
                                     """)
        self.popup_layout.addWidget(category_label)
        
        self.catComboBox = QCatComboBox("stat")
 
        self.catComboBox.currentIndexChanged.connect(self.update_icon)
        self.popup_layout.addWidget(self.catComboBox)
        
        self.popup_layout.setContentsMargins(20, 25, 20, 25)

        self.Inactive_icon = QIcon("assets/icons/filter_inactive_icon.svg")
        self.Active_icon = QIcon("assets/icons/filter_active_icon.svg")
        self.setIcon(self.Inactive_icon)
        self.setIconSize(QSize(24, 24))
    
    def update_icon(self, idx):
        innerdata = self.catComboBox.itemData(idx)
        if innerdata == -1:
            self.setIcon(self.Inactive_icon)
        else:
            self.setIcon(self.Active_icon)

class QStyledComboBox(QComboBox) :
    def __init__(self):
        super().__init__()
        self.setFixedWidth(160)
        self.setFixedHeight(30)
        self.setStyleSheet(
            """
            QComboBox {
                background-color: white; 
                color: black;
                border: 2px solid #D9D9D9;
                border-radius: 10px;
                padding-left: 5px;  
            }
            QComboBox::drop-down {
                width: 20px;
                background-color: transparent;
            }                   
            QComboBox::down-arrow {
                image: url(assets/icons/dropdown_icon.svg);
                background-color: transparent;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                outline: 0px;
                margin: 0px;
                padding: 0px;
                padding-top: 5px;
                padding-bottom: 5px;
                border: 2px solid #D9D9D9; 
                border-radius: 10px;

            }                
            QComboBox QAbstractItemView::item {
            background-color: transparent;
            color: black;
            padding: 5px;
            border: none;
    }
        """)
        view = self.view()
        view.parent().setObjectName("viewpare")
        view.parent().setStyleSheet("#viewpare{background-color: transparent;}")

class QCatComboBox(QStyledComboBox) :
    def __init__(self, typeOf = None):
        super().__init__()
        self.catList = fetchCatList("admin") 
        if typeOf == "stat" :
            self.addItem("All", -1)
        for cat in self.catList : 
            self.addItem(cat[1], cat[0])
        # this should listen to any category updates (not yet implemented)

    def setDefaultOption(self, cat_id) :
        for i in range(self.count()) :
            if int(self.itemData(i)) == int(cat_id) :
                self.setCurrentIndex(i)
                return 