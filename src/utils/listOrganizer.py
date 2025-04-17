import dateutil.parser as dparser
import os
import sys
sys.path.append(".")
from datetime import *;
from src.database.queries import fetchStatistics, fetchOrderHistory


def paginate(list) :
    pass

def organizeByDate(orderList) :
    orderListArr = [] 

    previousDate = datetime(1,1,1,1,1,1)
    for orderTuple in orderList :
        order_id, order_datetime = orderTuple
        order_datetime = str(order_datetime)
        orderdate = dparser.parse(order_datetime)

        if orderdate.day - previousDate.day != 0 : 
            # add header
            headerObj = {
                "content" : dateParser(order_datetime),
                "is_header" : True,
            }
            previousDate = orderdate
            orderListArr.append(headerObj)

        hourObj = {
            "content" : (hourParser(order_datetime), order_id),
            "is_header" : False,
        }      
        orderListArr.append(hourObj) 
    return orderListArr


def hourParser(datestr) :
    mydate = dparser.parse(datestr, fuzzy=True)
    hour = mydate.strftime('%I').lstrip('0')
    minutes = mydate.strftime('%M')
    ampm = mydate.strftime('%p')
    return f"{hour}:{minutes} {ampm}"

def dateParser(datestr) :
    note = None
    date = dparser.parse(datestr, fuzzy=True)
    now = datetime.now()
    delta = now.day - date.day
    if delta == 0 : 
        note = "Today"
    elif delta == 1 :
        note = "Yesterday"
    weekday = date.strftime('%A')
    month = date.strftime('%B')
    day = date.strftime("%d").lstrip('0')
    year = date.strftime('%Y')
    if note is not None :
        return f"{note} - {weekday}, {month} {day}, {year}"
    else :
        return f"{weekday}, {month} {day}, {year}"


print(dateParser("2025-04-07 04:19:37"))


orders = fetchOrderHistory()
organizedOrders = organizeByDate(orders)

for item in organizedOrders :
    print(item["content"])

