
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
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["#","Food", "Category", "Times Ordered"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.statistics_table(True)    
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 30)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
       
        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        


    def statistics_table(self, mostordered): 
        stats_data = fetchStatistics('DESC' if mostordered else 'ASC')
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
        super().__init__() 
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["#","Date", "OrderID", ""])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setShowGrid(False)
        self.order_table()
        self.verticalHeader().setVisible(False)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(3, 50)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStyleSheet("margin-right: 10px")
        self.viewport().setStyleSheet("margin-right: 10px")
        

    def order_table(self): 
        stats_data = fetchOrderHistory()
        self.setRowCount(len(stats_data))
        orders = fetchOrderHistory()
        self.setRowCount(len(orders) + 1)
        count = 1

        for row, order in enumerate(orders):
            order_id, order_datetime = order
            self.setItem(row, 0, QTableWidgetItem(str(count)))
            self.setItem(row, 1, QTableWidgetItem(str(order_datetime)))
            self.setItem(row, 2, QTableWidgetItem(str(order_id)))
            viewBtn = QPushButton("view")
            viewBtn.setFixedHeight(20)
            self.setCellWidget(row, 3, viewBtn)
            count+=1
  
    


