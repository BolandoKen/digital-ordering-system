
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
import math
from src.database.queries import fetchStatistics, fetchOrderHistory
from src.components.Dialogs import QviewOrderDialog
from src.utils.PubSub import pubsub
from src.utils.listOrganizer import organizeByDate, getPage
from src.components.PageNav import QPageNav
from src.components.Buttons import QOrderDetailsButton


class QStyledTable(QTableWidget) :
    def __init__(self) :
        super().__init__() 
        self.setStyleSheet("""
                QTableWidget {
                    border: none;     
                }
                QHeaderView::section {
                    background-color: white;
                    color: black;
                    padding: 4px;
                    border: none;
                    border-bottom: 1px solid black;
                    border-top: 1px solid black;
                }

                QTableWidget::item:selected {
                    background-color: #007acc;
                    color: white;
                }
                QScrollBar:vertical {
                    width: 10px;
                    margin: 0;
                    border: none;
                }
                QScrollBar::handle:vertical {
                    min-height: 10px;
                    border: none;
                    background-color: #D9D9D9;
                    border-radius: 5px;
                }
                QScrollArea {
                    padding: 0px;
                    border:none;
                    }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical,
                QScrollBar::up-arrow:vertical,
                QScrollBar::down-arrow:vertical{
                    background: none;
                    height: 0px; 
                    width: 0px                              
                }
                """)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)



class QStatsTable(QStyledTable) : 
    def __init__(self) :
        super().__init__() 
        self.search_term = None
        self.orderBy_mostOrdered = True
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["#","Food", "Category", "Times Ordered"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.init_list() 
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 30)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        pubsub.subscribe("orderSubmitted_event", self.statistics_table)
        pubsub.subscribe("updateFoodItem", self.statistics_table)

        self.rows = 25
        self.curr_lastPage = math.ceil(len(self.stats_data)/self.rows)
        self.pageNav = QPageNav(self.curr_lastPage, self.renderPage )
        self.renderPage()

    def setOrderBy(self, orderby) :
        self.orderBy_mostOrdered = orderby
        self.statistics_table()

    def renderPage(self) :
        paginatedArr = getPage(self.stats_data, self.pageNav.currentPage, self.rows)
        self.renderList(paginatedArr)

    def renderList(self, mylist) :
        self.setRowCount(len(mylist)) 
        count = (self.pageNav.currentPage - 1) * self.rows + 1

        for row, (food, category, times) in enumerate(mylist):
            self.setItem(row, 0, QTableWidgetItem(str(count)))
            self.setItem(row, 1, QTableWidgetItem(food)) 
            self.setItem(row, 2, QTableWidgetItem(category))
            self.setItem(row, 3, QTableWidgetItem(str(times)))
            count += 1  

    def init_list(self) :
        self.stats_data = fetchStatistics('DESC' if self.orderBy_mostOrdered else 'ASC', search_term=self.search_term)


    def updateStatsTable(self, category_id=None, mostordered=True, search_term=None): 
        self.search_term = search_term 
        order = "DESC" if mostordered else "ASC"
        self.stats_data = fetchStatistics(order, category_id, search_term)
        self.pageNav.updateNav(self.stats_data, self.rows)
        self.renderPage()

    def statistics_table(self, e = None): # redundant with function above?
        self.stats_data = fetchStatistics('DESC' if self.orderBy_mostOrdered else 'ASC', search_term=self.search_term)
        self.pageNav.updateNav(self.stats_data, self.rows)
        self.renderPage()
    
class QOrderHTable(QStyledTable) :
    def __init__(self) :
        # fetch all list -> paginate -> organize by date
        # possible feature, sticky headers
        super().__init__() 
        self.viewDialog = QviewOrderDialog(self.window())
        self.setColumnCount(3)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setShowGrid(False)
        self.init_list()
        self.verticalHeader().setVisible(False)
        self.filter = None

        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 50)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        pubsub.subscribe("orderSubmitted_event", self.order_table)

        self.rows = 50
        self.curr_lastPage = math.ceil(len(self.orders_list)/self.rows)
        self.pageNav = QPageNav(self.curr_lastPage, self.order_table )
        # self.order_table()

        self.set_filter(None)

    def organizePage(self, mylist) :
        paginatedOrders = getPage(mylist, self.pageNav.currentPage, self.rows)
        organizedOrders = organizeByDate(paginatedOrders)
        return organizedOrders

    def renderList(self, mylist) :
        count = 1
        mylist = self.organizePage(mylist)
        self.setRowCount(len(mylist))

        for row, item in enumerate(mylist):
            is_header = item["is_header"]
            if not is_header :
                order = item["content"]
                order_datetime, order_id = order
                self.setItem(row, 0, QTableWidgetItem(str(order_datetime)))
                self.setItem(row, 1, QTableWidgetItem(str(order_id)))
                viewBtn = QOrderDetailsButton()
                viewBtn.clicked.connect(lambda _, order_id = order_id : self.publishToDialog(order_id))
                viewBtn.setFixedHeight(20)
                self.setCellWidget(row, 2, viewBtn)
                count+=1
            else :
                #add header
                headerDateLabel = QLabel(item["content"])
                self.setCellWidget(row, 0, headerDateLabel)
                self.setSpan(row, 0,1,3)
                pass
    

    def order_table(self, e = None): 
        
        self.clearTable()
        self.setHorizontalHeaderLabels(["Date", "OrderID", ""])
        self.orders_list = fetchOrderHistory(self.filter)
        self.pageNav.updateNav(self.orders_list, self.rows)
        self.renderList(self.orders_list)
    
    def init_list(self) :
        self.orders_list = fetchOrderHistory()

    # for filter by date range, and display by # of rows,
    #  dont forget to call updateNav

    def publishToDialog(self, orderid) :
        pubsub.publish("viewClicked_event", orderid)
        self.viewDialog.exec()
    
    def clearTable(self) :
        for row in range(self.rowCount()) :
            for col in range(self.columnCount()) :
                widget = self.cellWidget(row,col) 
                if widget is not None :
                    widget.deleteLater()
        self.setRowCount(0)

    def set_filter(self, date_filter):
        self.filter = date_filter
        self.order_table()

  
    


