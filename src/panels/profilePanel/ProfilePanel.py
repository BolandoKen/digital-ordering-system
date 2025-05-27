import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
    QVBoxLayout,
    QScrollArea,
)
from src.utils.PixMap import setPixMapOf
from src.components.Headers import QOtherPanelHeader
from src.components.Table import QOrderHTable
from src.panels.profilePanel.ProfileEditSection import QProfile, QProfileViewState
from src.utils.PubSub import pubsub
from PyQt6.QtCore import Qt
from src.components.Calendar import QCalendarFilterFrame

class QProfilePanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.order_layout = QVBoxLayout(self)
        self.order_layout.setContentsMargins(0,0,0,0)
        self.order_layout.setSpacing(0)
        history_label = QLabel("Order History")
        history_label.setStyleSheet("background-color: white;color: #A1A1A1;padding: 4px;border: none;font-size: 30px;font-weight: bold;font-family: 'Helvetica'")
        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,0,10)
        self.calendarfilter = QCalendarFilterFrame("orders") # pass in {orders}_applyDateClicked

        self.label_filter_hbox = QHBoxLayout()
        self.label_filter_hbox.addWidget(history_label)
        self.label_filter_hbox.addStretch()
        self.label_filter_hbox.addWidget(self.calendarfilter)
        self.label_filter_hbox.addSpacing(10)

        self.orderHTable = QOrderHTable()
        contentsVLayout.addLayout(self.label_filter_hbox)
        contentsVLayout.addWidget(self.orderHTable)
        contentsVLayout.addWidget(self.orderHTable.pageNav, alignment=Qt.AlignmentFlag.AlignCenter )

        self.order_layout.addWidget(QOtherPanelHeader("Account"))
        self.order_layout.addWidget(QProfile(), alignment=Qt.AlignmentFlag.AlignTop)
        self.order_layout.addLayout(contentsVLayout)

        pubsub.subscribe("orders_applyDateClicked", self.filterOrdersByDate)

    def filterOrdersByDate(self, date):

        self.orderHTable.set_filter(date)
