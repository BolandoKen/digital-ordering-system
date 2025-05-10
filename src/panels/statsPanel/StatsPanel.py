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
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from PyQt6.QtCore import Qt
from src.database.queries import fetchStatistics
from src.components.Headers import QOtherPanelHeader
from src.components.Table import QStatsTable
from src.components.ComboBox import QCatComboBox, QFilterButton
from src.components.LineEdit import QSearchArea
from src.components.Calendar import QCalendarFilterFrame
from src.utils.PubSub import pubsub

class QStatsPanel(QFrame) :
    def __init__(self):
        super().__init__()
        self.stats_layout = QVBoxLayout(self)
        self.stats_layout.setContentsMargins(0,0,0,0)
        self.stats_layout.setSpacing(0)
        self.mostordered = True
        self.stats_setup()

    def stats_setup(self):
   
        self.stats_layout.addWidget(QOtherPanelHeader("Statistics"))
        self.search_area = QSearchArea(self, "stats")
        self.stats_layout.addWidget(self.search_area)
        self.search_area.searchbar.textChanged.connect(self.update_table)
        queryBarHLayout = QHBoxLayout()
        self.sort_btn = QPushButton("Show Least Ordered")
        self.sort_btn.clicked.connect(self.changeorder)


        self.catFilter = QFilterButton()
        self.catFilter.catComboBox.currentIndexChanged.connect(self.update_table)

        self.dateFilter = QCalendarFilterFrame("stats") # pass in {stats}_applyDateClicked

        queryBarHLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        queryBarHLayout.addWidget(self.sort_btn)
        queryBarHLayout.addStretch()
        queryBarHLayout.addWidget(self.dateFilter)
        queryBarHLayout.addSpacing(10)
        queryBarHLayout.addWidget(self.catFilter)
        queryBarHLayout.addSpacing(20)



        contentsVLayout = QVBoxLayout()
        contentsVLayout.setContentsMargins(10,10,0,10)
        contentsVLayout.setSpacing(5)

        self.table = QStatsTable() 
    
        contentsVLayout.addLayout(queryBarHLayout)
        contentsVLayout.addWidget(self.table)
        contentsVLayout.addWidget(self.table.pageNav, alignment=Qt.AlignmentFlag.AlignCenter)
        self.stats_layout.addLayout(contentsVLayout)
        pubsub.subscribe("stats_applyDateClicked", self.apply_dateFilter)
        self.search_term = None
        # self.update_table()

    def apply_dateFilter(self, e = None) : 
        self.update_table()

    
    def changeorder(self):
        self.mostordered = not self.mostordered
        if self.mostordered:
            self.sort_btn.setText("Show Least Ordered")
        else:
            self.sort_btn.setText("Show Most Ordered")
        self.search_term = self.search_area.searchbar.text().strip()
        self.update_table(self.search_term)

    def update_table(self, search_term = None):
        category_id = self.catFilter.catComboBox.itemData(self.catFilter.catComboBox.currentIndex())
        if category_id == -1:
            category_id = None

        search_term = self.search_area.searchbar.text().strip()
        self.search_term = None if search_term == "" or search_term is None else search_term
        self.table.updateStatsTable(category_id, self.mostordered, self.search_term, self.dateFilter.getDate())
    
