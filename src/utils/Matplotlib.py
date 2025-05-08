
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import QDate
from datetime import date, timedelta, datetime, time
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

            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            ax.set_title('No orders..')

            self.draw()
            return
        if len(foodstats) == 1 and isinstance(foodstats[0][0], date) : # if only has one day, defaults to display on that single day
            start = foodstats[0][0]
            self.DateRange = QDate(start.year, start.month, start.day)
            foodstats = fetchStatsOfFoodItem(self.fooditem_id, self.DateRange)
        if isinstance(self.DateRange, QDate) : 
            self.plotSpecificDate(self.DateRange, foodstats)
            return
        
        elif self.DateRange is None : # defaults to first and recent ordered date 
            start = foodstats[0][0]
            start = QDate(start.year, start.month, start.day)
            end = foodstats[len(foodstats) - 1][0]
            end = QDate(end.year, end.month, end.day)
        else : # instance of Tuple : specified daterange
            start = self.DateRange[0]
            end = self.DateRange[1]
        
        self.plotDateRange(start, end, foodstats)

    def plotSpecificDate(self, mydate, foodstats) :
        mydate_converted = date(mydate.year(), mydate.month(), mydate.day()) if isinstance(mydate, QDate) else mydate
        x_hours = []
        y_count = []
        highlight_indices = []

        currenthour = 0 
        end = 23

        idx_foodstatsHour = 0 
        loop_idx = 0
        while currenthour < end :
            if idx_foodstatsHour < len(foodstats) and int(foodstats[idx_foodstatsHour][0]) == currenthour :
                y_count.append(int(foodstats[idx_foodstatsHour][1]))
                idx_foodstatsHour +=1 
                highlight_indices.append(loop_idx)
            else :
                y_count.append(0)
            x_hours.append(datetime.combine(mydate_converted, time(currenthour)))
            currenthour += 1
            loop_idx += 1

        print(x_hours)
        print(y_count)
        print(highlight_indices)
        self.fig.clear()
        ax = self.fig.add_subplot()
     
        highlight_x = [x_hours[i] for i in highlight_indices]
        highlight_y = [y_count[i] for i in highlight_indices]
        ax.plot_date(x_hours, y_count,'None', linestyle='solid', color='#c8161d')
        ax.plot_date(highlight_x, highlight_y, color='#c8161d', linestyle='None', picker=5)

        date_format = mpl_dates.DateFormatter('%I %p')
        ax.xaxis.set_major_formatter(date_format)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        self.fig.autofmt_xdate()
        ax.tick_params(axis='x', which='major', labelsize=7)
        ax.set_xlabel('Hours') 
        
        smonth, sday, syear = self.parsetoString(mydate_converted)


        ax.set_title(f'{smonth} {sday} {syear}') # change this

        self.draw()
        pass
    
    def plotDateRange(self, start,end, foodstats) :
        x_dates = []
        y_count = []
        highlight_indices = []
        current = start
        idx_foodstatsDate = 0 # points to foodstats, checks for same dates to assign inside loop
        loop_idx = 0
        while current <= end:
            currentdate_converted = date(current.year(), current.month(), current.day()) if isinstance(current, QDate) else current
            
            if idx_foodstatsDate < len(foodstats) and foodstats[idx_foodstatsDate][0] == currentdate_converted :
                y_count.append(int(foodstats[idx_foodstatsDate][1]))
                idx_foodstatsDate +=1
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

        if len(x_dates) <= 1 : # set min max limits to avoid range by year ; i think now this is unused?
            mindate = x_dates[0] - timedelta(days=1)
            maxdate = x_dates[0] + timedelta(days=1)
            ax.set_xlim([mindate, maxdate])

        date_format = mpl_dates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(date_format)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        self.fig.autofmt_xdate()
        ax.tick_params(axis='x', which='major', labelsize=7)
        ax.set_xlabel('Day')

        smonth, sday, syear = self.parsetoString(start)
        emonth, eday, eyear = self.parsetoString(end)
        if syear == eyear :
            ax.set_title(f'{smonth} {sday} to {emonth} {eday} of {eyear}') 
        else :
            ax.set_title(f'{smonth} {sday}, {syear} to {emonth} {eday}, {eyear}')

        self.draw()
        
    def parsetoString(self, mydate) :
        mydate_converted = date(mydate.year(), mydate.month(), mydate.day()) if isinstance(mydate, QDate) else mydate
        smonth = mydate_converted.strftime('%B')
        sday = mydate_converted.strftime("%d").lstrip('0')
        syear = mydate_converted.strftime('%Y')
        return (smonth, sday, syear)
        