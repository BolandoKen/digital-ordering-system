
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import QDate
from datetime import date, timedelta
from src.database.queries import fetchStatsOfFoodItem
from matplotlib import dates as mpl_dates
from matplotlib.ticker import MaxNLocator


class lineGraphCanvas(FigureCanvasQTAgg) :
    def __init__(self) :
        self.fig = Figure()
        super().__init__(self.fig)

    def setContents(self, fooditem_id, DateRange) :
        # self.DateRange = (QDate(2025, 4, 1), QDate(2025, 5, 6))
        self.DateRange = DateRange
        self.fooditem_id = fooditem_id
        foodstats = fetchStatsOfFoodItem(self.fooditem_id, self.DateRange)
        if len(foodstats) == 0 :
            self.fig.clear()
            ax = self.fig.add_subplot()

            date_format = mpl_dates.DateFormatter('%m/%d')
            ax.xaxis.set_major_formatter(date_format)
            
            self.fig.autofmt_xdate()
            ax.tick_params(axis='x', which='major', labelsize=7)
            ax.set_xlabel('Date')
            ax.set_title('April 1 to May 6')

            self.draw()
            return
        if DateRange is None : # defaults to first and recent ordered date 
            start = foodstats[0][0]
            start = QDate(start.year, start.month, start.day)
            end = foodstats[len(foodstats) - 1][0]
            end = QDate(end.year, end.month, end.day)
        elif isinstance(self.DateRange, QDate) : 
            self.plotSpecificDate()
            pass
        else : # instance of Tuple : specified daterange
            start = self.DateRange[0]
            end = self.DateRange[1]
        
        self.plotDateRange(start, end, foodstats)

    def plotSpecificDate(self) :
        pass
    
    def plotDateRange(self, start,end, foodstats) :
        x_dates = []
        y_count = []
        highlight_indices = []
        current = start
        idx = 0 
        loop_idx = 0
        while current <= end:

            currentdate_converted = date(current.year(), current.month(), current.day()) if isinstance(current, QDate) else current
            
            if idx < len(foodstats) and foodstats[idx][0] == currentdate_converted :
                y_count.append(int(foodstats[idx][1]))
                idx +=1
                highlight_indices.append(loop_idx)
            else :
                y_count.append(0)                
            x_dates.append(currentdate_converted)
            current = current.addDays(1)
            loop_idx +=1
        self.fig.clear()
        ax = self.fig.add_subplot()
     
        highlight_x = [x_dates[i] for i in highlight_indices]
        highlight_y = [y_count[i] for i in highlight_indices]
        ax.plot_date(x_dates, y_count,'None', linestyle='solid', color='#c8161d')
        ax.plot_date(highlight_x, highlight_y, color='#c8161d', linestyle='None', picker=5)

        if len(x_dates) <= 1 : # set min max limits to avoid range by year
            mindate = x_dates[0] - timedelta(days=1)
            maxdate = x_dates[0] + timedelta(days=1)
            ax.set_xlim([mindate, maxdate])

        date_format = mpl_dates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(date_format)
        
        self.fig.autofmt_xdate()
        ax.tick_params(axis='x', which='major', labelsize=7)
        ax.set_xlabel('Date') # change this
        ax.set_title('April 1 to May 6') # change this

        self.draw()
        
        