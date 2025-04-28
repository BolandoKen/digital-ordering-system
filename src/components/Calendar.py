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
    QCalendarWidget,
    QDateEdit,
)
from PyQt6.QtWidgets import QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QMouseEvent, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from src.components.MenuCards import QMenuCard
from src.utils.PixMap import setPixMapOf
from src.components.ComboBox import QPopupButton, QStyledComboBox
from PyQt6.QtCore import QDate

class QMyDateEdit(QDateEdit) :
    def __init__(self) :
        super().__init__()
        self.setFixedWidth(100)
        self.setCalendarPopup(True)

class QCalendarFilter(QPopupButton) :
    dateSelected = pyqtSignal(object) #fix suggested by gpt, to use object instead of QDate
    def __init__(self) :
        super().__init__()
        self.popup_layout.setContentsMargins(10,10,10,10)
        self.mycalendar = QCalendarWidget()
        self.popup.setFixedHeight(100)
        self.container.setGeometry(0,0,193,100)
        
        self.calendar_icon = QIcon("assets/icons/calendar_icon.svg")
        self.setIcon(self.calendar_icon)
        self.setIconSize(QSize(24, 24))
        self.combobox = QStyledComboBox()
        self.combobox.addItems(['None', 'Specific Date', 'Date Range'])
        
        self.specdate = QSpecDate()
        self.daterange = QDateRangeFields()
        self.popup_layout.addWidget(self.combobox)
        self.popup_layout.addWidget(self.specdate)
        self.popup_layout.addWidget(self.daterange)
        self.popup_layout.addStretch()

        self.apply =  QPushButton("apply filter")
        self.apply.setStyleSheet("background-color: white; color: black; border: 1px solid #a1a1a1; padding:5px; border-radius: 5px;")
        self.popup_layout.addWidget(self.apply, alignment=Qt.AlignmentFlag.AlignLeft)
        self.popup_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.combobox.currentTextChanged.connect(self.handleComboBoxChanged)
        self.specdate.hide() 
        self.daterange.hide()

        self.apply.clicked.connect(self.apply_filter)

    def handleComboBoxChanged(self, text) :
        self.specdate.hide() 
        self.daterange.hide()
        self.popup.setFixedHeight(100)
        self.container.setFixedHeight(100)
        if text == "Specific Date" :
            self.specdate.show()
            self.popup.setFixedHeight(130)
            self.container.setFixedHeight(130)
        elif text == "Date Range" :
            self.daterange.show()
            self.popup.setFixedHeight(160)
            self.container.setFixedHeight(160)

    def emit_date_selected(self, selected_date):
        selected_date = self.mycalendar.selectedDate()
        self.dateSelected.emit(selected_date)

    def apply_filter(self):
        selected_filter = self.combobox.currentText()
        if selected_filter == "Specific Date":
            selected_date = self.specdate.dateedit.date()
            self.dateSelected.emit(selected_date)
        elif selected_filter == "Date Range":
            start_date = self.daterange.fromdateedit.date()
            end_date = self.daterange.todateedit.date()
            self.dateSelected.emit((start_date, end_date))
          
        else:
            self.dateSelected.emit(None)

class QSpecDate(QFrame) :
    def __init__(self) :
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.setStyleSheet("background-color: white; color: #a1a1a1")
        
        datelabel = QLabel("on")
        self.dateedit = QDateEdit()
        self.dateedit.setCalendarPopup(True)
        self.dateedit.setDate(QDate.currentDate())

        self.main_layout.addWidget(datelabel)
        self.main_layout.addWidget(self.dateedit)

class QDateRangeFields(QFrame) :
    def __init__(self) :
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet("background-color: white; color: #a1a1a1")
        
        from_hbox = QHBoxLayout()
        from_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fromlabel = QLabel("from")
        self.fromdateedit = QDateEdit()
        from_hbox.addWidget(fromlabel)
        from_hbox.addStretch()
        from_hbox.addWidget(self.fromdateedit)

        to_hbox = QHBoxLayout()
        to_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tolabel = QLabel("to")
        self.todateedit = QDateEdit()
        to_hbox.addWidget(tolabel)
        to_hbox.addStretch()
        to_hbox.addWidget(self.todateedit)

        self.fromdateedit.setCalendarPopup(True)
        self.todateedit.setCalendarPopup(True)
        self.fromdateedit.setDate(QDate.currentDate())
        self.todateedit.setDate(QDate.currentDate())

        self.main_layout.addLayout(from_hbox)
        self.main_layout.addLayout(to_hbox)