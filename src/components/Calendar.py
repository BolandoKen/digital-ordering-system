from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QFrame,
    QCalendarWidget,
    QDateEdit,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize,  QRect
from src.components.ComboBox import QPopupButton
from PyQt6.QtCore import QDate
from src.utils.PubSub import pubsub
from datetime import date

class QMyDateEdit(QDateEdit) :
    def __init__(self) :
        super().__init__()
        self.setFixedWidth(100)
        self.setCalendarPopup(True)

class QCalendarFilterFrame(QFrame) :
    def __init__(self, pubsub_type = None) :
        super().__init__()
        main_layout = QHBoxLayout(self)
        self.dateLabel = QLabel("All Time")
        self.dateLabel.setStyleSheet("font-family: Helvetica; font: 15px;")
        self.calendarFilterBtn = QCalendarFilter(pubsub_type)
        self.calendarFilterBtn.dateoptionsframe.applybtn.clicked.connect(self.setDateLabel)
        main_layout.addWidget(self.dateLabel)
        main_layout.addWidget(self.calendarFilterBtn)
    
    def setDateLabel(self) :
        mydate = self.calendarFilterBtn.dateoptionsframe.getDate()
        self.dateLabel.hide()
        if isinstance(mydate, QDate) :
            monthfm, dayfm, yearfm = self.parseDate(mydate)
            self.dateLabel.setText(f"{monthfm} {dayfm}, {yearfm}")
        elif isinstance(mydate, tuple) :
            start_monthfm, start_dayfm, start_yearfm = self.parseDate(mydate[0])
            end_monthfm, end_dayfm, end_yearfm = self.parseDate(mydate[1])
            start_datestr = f"{start_monthfm} {start_dayfm}, {start_yearfm}" if start_yearfm != end_yearfm else f"{start_monthfm} {start_dayfm}" 
            end_datestr = f"{end_monthfm} {end_dayfm}, {end_yearfm}"
            final_datestr = f"{start_datestr} – {end_datestr}"
            self.dateLabel.setText(final_datestr)
        elif mydate is None :
            self.dateLabel.setText("All Time")
        self.dateLabel.show() # bcus of visual glitches when changing text

    def parseDate(self, mydate) :
        mydate_converted = date(mydate.year(), mydate.month(), mydate.day()) if isinstance(mydate, QDate) else mydate
        monthfm = mydate_converted.strftime('%b')
        dayfm = mydate_converted.strftime("%d").lstrip('0')
        yearfm = mydate_converted.strftime('%Y')
        return (monthfm, dayfm, yearfm)

    def getDate(self) :
        return self.calendarFilterBtn.getDate()
    
class QCalendarFilter(QPopupButton) :
    def __init__(self, pubsub_type = None) :
        super().__init__()
        self.popup_layout.setContentsMargins(10,10,10,10)
        self.mycalendar = QCalendarWidget()
        self.popup.setFixedSize(270, 220)
        self.container.setGeometry(0,0,270,220)
        
        self.calendar_icon = QIcon("assets/icons/calendar_icon.svg")
        self.setIcon(self.calendar_icon)
        self.setIconSize(QSize(24, 24))
        
        self.dateoptionsframe = QDateOptionsFrame(pubsub_type, self)
        self.popup_layout.addWidget(self.dateoptionsframe)
    
    def getDate(self) :
        return self.dateoptionsframe.getDate()

class QDateOptionsFrame(QFrame) :
    def __init__(self, pubsub_type = None, parent_filterbtn = None) :
        super().__init__()
        self.setStyleSheet("background-color: white; color: black;")
        self.pubsub_type = pubsub_type
        main_layout = QVBoxLayout(self)

        self.nullDateEdit = QCustomNullableDateEdit()

        self.nullDateEdit2 = QCustomNullableDateEdit()

        hbox0 = QHBoxLayout()
        hbox0.addWidget(QLabel("from"))
        hbox0.addWidget(QLabel("to"))


        grid = QGridLayout()
        grid.addWidget(QLabel("from"), 0, 0 )
        grid.addWidget(QLabel("to"), 0, 2 )
        grid.addWidget(self.nullDateEdit, 1, 0 )
        grid.addWidget(QLabel("-"), 1, 1 )
        grid.addWidget(self.nullDateEdit2, 1, 2)


        self.applybtn = QPushButton("Apply")
        self.applybtn.clicked.connect(self.handleApplyBtn)
        clearbtn = QPushButton("Clear")
        clearbtn.clicked.connect(self.handleClearBtn)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.applybtn)
        hbox2.addWidget(clearbtn)

        todaybtn = QPushButton("Today")

        lastweekbtn = QPushButton("Last Week")
        weekbtn = QPushButton("This Week")
        weekhbox = QHBoxLayout()
        weekhbox.addWidget(lastweekbtn)
        weekhbox.addWidget(weekbtn)

        monthhbox = QHBoxLayout()
        lastmonthbtn = QPushButton("Last Month")
        monthbtn = QPushButton("This Month")   
        monthhbox.addWidget(lastmonthbtn) 
        monthhbox.addWidget(monthbtn)

        todaybtn.clicked.connect(self.handleTodayBtn)
        lastweekbtn.clicked.connect(self.handleLastWeekBtn)
        weekbtn.clicked.connect(self.handleWeekBtn)
        lastmonthbtn.clicked.connect(self.handleLastMonthBtn)
        monthbtn.clicked.connect(self.handleMonthBtn)

        main_layout.addLayout(grid)
        main_layout.addWidget(todaybtn)
        main_layout.addLayout(weekhbox)
        main_layout.addLayout(monthhbox)
        main_layout.addLayout(hbox2)

    def handleClearBtn(self) :
        self.nullDateEdit.clear()
        self.nullDateEdit2.clear()
    
    def handleTodayBtn(self) :
        self.nullDateEdit.setDate(QDate.currentDate())
        self.nullDateEdit.setFloaterText()
        self.nullDateEdit2.clear()

    def handleWeekBtn(self):
        today = QDate.currentDate()
        day_of_week = today.dayOfWeek()  # Monday = 1, Sunday = 7

        start_of_week = today.addDays(-day_of_week + 1)  # Monday
        end_of_week = start_of_week.addDays(6)           # Sunday

        self.nullDateEdit.setDate(start_of_week)
        self.nullDateEdit.setFloaterText()
        self.nullDateEdit2.setDate(end_of_week)

    def handleMonthBtn(self):
        today = QDate.currentDate()
        start_of_month = QDate(today.year(), today.month(), 1)
        end_of_month = start_of_month.addMonths(1).addDays(-1)

        self.nullDateEdit.setDate(start_of_month)
        self.nullDateEdit2.setDate(end_of_month)

    def handleLastWeekBtn(self):
        today = QDate.currentDate()
        day_of_week = today.dayOfWeek()  # Monday = 1, Sunday = 7

        start_of_this_week = today.addDays(-day_of_week + 1)
        start_of_last_week = start_of_this_week.addDays(-7)
        end_of_last_week = start_of_this_week.addDays(-1)

        self.nullDateEdit.setDate(start_of_last_week)
        self.nullDateEdit2.setDate(end_of_last_week)

    def handleLastMonthBtn(self):
        today = QDate.currentDate()
        this_month_start = QDate(today.year(), today.month(), 1)
        last_month_end = this_month_start.addDays(-1)
        last_month_start = QDate(last_month_end.year(), last_month_end.month(), 1)

        self.nullDateEdit.setDate(last_month_start)
        self.nullDateEdit2.setDate(last_month_end)

    def handleApplyBtn(self) :
        date = self.getDate()
        pubsub.publish(f"{self.pubsub_type}_applyDateClicked", date)
    
    def getDate(self) :
        date = {"fromDate" : self.nullDateEdit.getValue(),
                "toDate": self.nullDateEdit2.getValue()
                }
        if date["fromDate"] is None and date["toDate"] is not None :
            return
        if date["fromDate"] is None : # if none, guarantees that it is clear date
            date = None
        elif date["toDate"] is None :
            date = date["fromDate"]
        else :
            date = (date["fromDate"],date["toDate"] )
        return date

class QCustomNullableDateEdit(QDateEdit) : 
    def __init__(self) :
        super().__init__()
        self.setStyleSheet(
            """
            * {
                background-color: white;
                border: none;
                color: black;
            }
            QDateEdit::drop-down {
                border:none;
                border-radius: 10px;
            }
        """)
        self.setFixedSize(110, 30)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())

        self.nullable_floater = QNullableFloater(self) 
        self.nullable_floater.move(0,0)
        self.nullable_floater.show()

        self.dateChanged.connect(self.setFloaterText)
       
        
    def keyPressEvent(self, e):
       return

    def mousePressEvent(self, event):
        restricted_area = QRect(0, 0, self.width() - 15, self.height())  # example: block left side
        if restricted_area.contains(event.pos()):
            event.ignore()  
            print("ignored")
        else:
            self.setFloaterText()
            super().mousePressEvent(event)

    def setFloaterText(self) :
        datestr = self.date().toString("yyyy-MM-dd")
        self.nullable_floater.setText(datestr) 

    def getValue(self) :
        if self.nullable_floater.text() == "-" :
            return None
        else : 
            return self.date()

    def clear(self) :
        self.setDate(QDate.currentDate())
        self.nullable_floater.setText("-")

class QNullableFloater(QFrame) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.setFixedSize(110, 30)
        self.setObjectName("nullable")
        self.setStyleSheet("*{border: 1px solid #d1d1d1; border-radius: 10px;} #nullable:focus {border: 1px solid orange;}")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.label = QLabel("-")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border:none; background: transparent;")
        
        self.dropBtn = QPushButton() 
        self.dropBtn.setIcon(QIcon("assets/icons/dropdown_icon.svg"))
        self.dropBtn.setIconSize(QSize(10,10))
        self.dropBtn.setStyleSheet("border: none; border-radius: 0px; border-top-right-radius: 10px; border-bottom-right-radius: 10px;")
        self.dropBtn.setFixedSize(20,28)
        self.dropBtn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.dropBtn)

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def keyPressEvent(self, e):
        print("hi")
        if e.key() == Qt.Key.Key_Backspace:
            self.label.setText("-")
        return super().keyPressEvent(e)

    def setText(self, text) :
        self.label.setText(text)
    
    def text(self) :
        return self.label.text()