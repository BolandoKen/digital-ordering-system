
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
from src.database.queries import fetchStatistics, fetchOrderHistory
from src.components.Dialogs import QviewOrderDialog
from src.utils.PubSub import pubsub
from src.utils.listOrganizer import organizeByDate


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
        self.orderBy_mostOrdered = True
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["#","Food", "Category", "Times Ordered"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.statistics_table()    
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 30)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        pubsub.subscribe("orderSubmitted_event", self.statistics_table)
        pubsub.subscribe("updateFoodItem", self.statistics_table)

    def setOrderBy(self, orderby) :
        self.orderBy_mostOrdered = orderby
        self.statistics_table()

    def updateStatsTable(self, category_id=None, mostordered=True):
        order = ("DESC" if mostordered else "ASC")
        stats = fetchStatistics(order, category_id)
        self.setRowCount(len(stats))
        count = 1 

        for row_id, row_data in enumerate(stats):
            food, category, times = row_data
            self.setItem(row_id, 0, QTableWidgetItem(str(count)))
            self.setItem(row_id, 1, QTableWidgetItem(food)) 
            self.setItem(row_id, 2, QTableWidgetItem(category))
            self.setItem(row_id, 3, QTableWidgetItem(str(times)))
            count += 1 #i might change this later, muni gi suggest sa chatgpt, ako orig code kay somehow na shift to the left tanan values after nako i-change ang category

    def statistics_table(self, e = None): 
        stats_data = fetchStatistics('DESC' if self.orderBy_mostOrdered else 'ASC')
        self.setRowCount(len(stats_data))
        count = 1
        for row, (food, category, times) in enumerate(stats_data): 
            self.setItem(row, 0, QTableWidgetItem(str(count)))
            self.setItem(row, 1, QTableWidgetItem(food))
            self.setItem(row, 2, QTableWidgetItem(category))
            self.setItem(row, 3, QTableWidgetItem(str(times)))
            count+=1
    
class QOrderHTable(QStyledTable) :
    def __init__(self) :
        # fetch all list -> paginate -> organize by date
        # possible feature, sticky headers
        super().__init__() 
        self.viewDialog = QviewOrderDialog()
        self.setColumnCount(3)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setShowGrid(False)
        self.order_table()
        self.verticalHeader().setVisible(False)

        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 50)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        pubsub.subscribe("orderSubmitted_event", self.order_table)
        

    def order_table(self, e = None): 
        self.clearTable()
        self.setHorizontalHeaderLabels(["Date", "OrderID", ""])
        orders = fetchOrderHistory()
        organizedOrders = organizeByDate(orders)
        count = 1
        self.setRowCount(len(organizedOrders))


        for row, item in enumerate(organizedOrders):
            is_header = item["is_header"]
            if not is_header :
                order = item["content"]
                order_datetime, order_id = order
                self.setItem(row, 0, QTableWidgetItem(str(order_datetime)))
                self.setItem(row, 1, QTableWidgetItem(str(order_id)))
                viewBtn = QPushButton("view")
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

  
    


