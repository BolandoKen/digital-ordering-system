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

class QFilterButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(40, 40)
        
        self.Inactive_icon = QIcon("assets/icons/filter_inactive_icon.svg")
        self.Active_icon = QIcon("assets/icons/filter_active_icon.svg")
        self.setIcon(self.Inactive_icon)
        self.setIconSize(QSize(24, 24))
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
        self.popup.setFixedSize(193, 126)
        self.popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.popup.setStyleSheet("""
            background-color: white; 
            border: 2px solid #D9D9D9; 
            border-radius: 10px;
            outline: none;
        """)

        container = QWidget(self.popup)
        container.setGeometry(0, 0, 193, 126)
        container.setStyleSheet("""
            background-color: white; 
            border: 2px solid #D9D9D9; 
            border-radius: 10px;
        """)
        
        popup_layout = QVBoxLayout()
        
        category_label = QLabel("Category")
        category_label.setStyleSheet("""
                                     background-color: white;
                                     color: black;
                                     font-family: Helvetica;
                                     font-size: 20px; font-weight: regular;
                                     border: none;
                                     border-radius: 0px;
                                     """)
        popup_layout.addWidget(category_label)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(["All", "Food", "Beverages", "Desserts"])
        self.combo_box.setFixedWidth(160)
        self.combo_box.setFixedHeight(30)
        self.combo_box.setStyleSheet("""
            QComboBox {
                color: black;
                border: 2px solid #D9D9D9;
                padding: 5px;  
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
                border: none;
            }                
            QComboBox QAbstractItemView::item {
            background-color: transparent;
            color: black;
            padding: 5px;
            border: none;
    }
        """)
        self.combo_box.currentTextChanged.connect(self.update_icon)
        popup_layout.addWidget(self.combo_box)
        
        popup_layout.setContentsMargins(20, 25, 20, 25)
        self.popup.setLayout(popup_layout)
    
        self.clicked.connect(self.toggle_popup)
    
    def toggle_popup(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            button_pos = self.mapToGlobal(QPoint(-152, self.height()))
            self.popup.move(button_pos)
            self.popup.show()

    def update_icon(self, text):
        if text == "All":
            self.setIcon(self.Inactive_icon)
        else:
            self.setIcon(self.Active_icon)

class QCatComboBox(QComboBox) :
    def __init__(self, typeOf = None):
        super().__init__()
        self.catList = fetchCatList("admin") 
        if typeOf == "stat" :
            self.addItem("no filter")
        for cat in self.catList : 
            self.addItem(cat[1], cat[0])
        # this should listen to any category updates (not yet implemented)

    def setDefaultOption(self, cat_id) :
        for i in range(self.count()) :
            if int(self.itemData(i)) == int(cat_id) :
                self.setCurrentIndex(i)
                return 