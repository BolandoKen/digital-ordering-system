
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import QDate
from datetime import date, timedelta, datetime, time
from src.database.queries import fetchStatsOfFoodItem
from matplotlib import dates as mpl_dates
from matplotlib.ticker import MaxNLocator



class lineGraphCanvas(FigureCanvasQTAgg) :
    def __init__(self) :
        self.fig = Figure()
        super().__init__(self.fig)
        self.typeOf = None
        self.peak = None

    def setContents(self, fooditem_id, DateRange) :
        self.decidePlotType(fooditem_id, DateRange)
        self.setAnnotates()
    
    def setAnnotates(self) :
        if self.typeOf == "specific_date" :
            peak = max(self.foodstats, key= lambda x: x[1])
            hourdatetime = datetime.strptime(str(peak[0]), '%H')# peak 0 would be int 
            hourdatetime_add = hourdatetime + timedelta(hours=1)
            hour = hourdatetime.strftime('%I %p').lstrip('0')
            hour2 = hourdatetime_add.strftime('%I %p').lstrip('0')
            peakhour_str = f'Peak ({hour} – {hour2}) : {peak[1]} orders'
            self.peak = peakhour_str
           
        elif self.typeOf == "date_range" :
            peak = max(self.foodstats, key= lambda x: x[1])
            monthfm = peak[0].strftime('%b')
            dayfm = peak[0].strftime('%d').lstrip('0')
            peakdate_str = f'Peak ({monthfm} {dayfm}) : {peak[1]} orders'
            self.peak = peakdate_str

        else :
            self.peak = ''
        print(self.peak)

    def decidePlotType(self, fooditem_id, DateRange) :
        self.DateRange = DateRange
        self.fooditem_id = fooditem_id
        self.foodstats = fetchStatsOfFoodItem(self.fooditem_id, self.DateRange)
        if len(self.foodstats) == 0 :
            self.fig.clear()
            ax = self.fig.add_subplot()

            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            ax.set_title('No orders..')

            self.draw()
            self.typeOf = None
            self.mytitle = 'No dates to show..'
            return
        if len(self.foodstats) == 1 and isinstance(self.foodstats[0][0], date) : # if only has one day, defaults to display on that single day
            start = self.foodstats[0][0]
            self.DateRange = QDate(start.year, start.month, start.day)
            self.foodstats = fetchStatsOfFoodItem(self.fooditem_id, self.DateRange)
            self.typeOf = "specific_date"
        if isinstance(self.DateRange, QDate) : 
            self.plotSpecificDate(self.DateRange, self.foodstats)
            self.typeOf = "specific_date"
            return
        elif self.DateRange is None : # defaults to first and recent ordered date 
            start = self.foodstats[0][0]
            start = QDate(start.year, start.month, start.day)
            end = self.foodstats[len(self.foodstats) - 1][0]
            end = QDate(end.year, end.month, end.day)
        else : # instance of Tuple : specified daterange
            start = self.DateRange[0]
            end = self.DateRange[1]

        self.typeOf = "date_range"
        self.plotDateRange(start, end, self.foodstats)

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
        
        smonth, sday, syear, _ = self.parsetoString(mydate_converted)

        self.mytitle = f'{smonth} {sday}'
        ax.set_title(f'{smonth} {sday} {syear}') 

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

        smonth, sday, syear, asmonth = self.parsetoString(start)
        emonth, eday, eyear, aemonth = self.parsetoString(end)
        if syear == eyear :
            ax.set_title(f'{smonth} {sday} – {emonth} {eday}, {eyear}') 
            self.mytitle = f'{asmonth} {sday} – {aemonth} {eday}, {eyear}'
        else :
            ax.set_title(f'{smonth} {sday}, {syear} – {emonth} {eday}, {eyear}')
            self.mytitle = f'{asmonth} {sday}, {syear} – {aemonth} {eday}, {eyear}'

        self.draw()
        
    def parsetoString(self, mydate) :
        mydate_converted = date(mydate.year(), mydate.month(), mydate.day()) if isinstance(mydate, QDate) else mydate
        smonth = mydate_converted.strftime('%B')
        sday = mydate_converted.strftime("%d").lstrip('0')
        syear = mydate_converted.strftime('%Y')
        abbrevmonth = mydate_converted.strftime('%b')
        return (smonth, sday, syear, abbrevmonth)
