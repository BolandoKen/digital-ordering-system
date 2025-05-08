from src.database.init_db import get_dbCursor
from PyQt6.QtCore import QDate
import traceback

cursor = get_dbCursor()

def fetchCatList(pageName) :
    if pageName == "admin" :
        cursor.execute("""SELECT c.category_id, c.name, c.imgfile
                       FROM Categories AS c
                       LEFT JOIN FoodItems AS f
                       on c.category_id = f.category_id
                       GROUP BY c.category_id
                       ORDER BY COUNT(IF(f.is_available = 1, 1, NULL)) DESC
                       """)
    elif pageName == "customer" :
        cursor.execute("""SELECT c.category_id, c.name, c.imgfile
                    FROM Categories AS c
                    LEFT JOIN FoodItems AS f
                    ON c.category_id = f.category_id
                    WHERE f.is_available = 1
                    GROUP BY c.category_id
                    HAVING COUNT(f.fooditem_id)!= 0
                    """)
    results = cursor.fetchall()
    return results

def fetchCategoryItemCount() :
    cursor.execute("""SELECT COUNT(f.fooditem_id)
                   FROM Categories AS c 
                   LEFT JOIN FoodItems AS f 
                   ON c.category_id = f.category_id 
                   GROUP BY c.category_id
                   """)
    return len(cursor.fetchall())

def fetchCategoryAvailableItemCount(category_id) :
    cursor.execute("""SELECT COUNT(f.fooditem_id)
                   FROM Categories AS c 
                   LEFT JOIN FoodItems AS f 
                   ON c.category_id = f.category_id 
                   WHERE f.is_available = 1
                   AND c.category_id = %s
                   """, (category_id,))
    return cursor.fetchone()[0]

def fetchCategoryUnavailableItemCount(category_id) :
    cursor.execute("""SELECT COUNT(f.fooditem_id)
                   FROM Categories AS c 
                   LEFT JOIN FoodItems AS f 
                   ON c.category_id = f.category_id 
                   WHERE f.is_available = 0
                   AND c.category_id = %s
                   """, (category_id,))
    return cursor.fetchone()[0]

def fetchFoodUnderCatList(category_id, showUnavailable = False) :
    if showUnavailable :
        cursor.execute(f"SELECT fooditem_id, name, price, imgfile, is_available, category_id FROM FoodItems WHERE category_id = {category_id} ORDER BY is_available DESC")
    else :
        cursor.execute(f"SELECT fooditem_id, name, price, imgfile, is_available, category_id FROM FoodItems WHERE category_id = {category_id} AND is_available = {not showUnavailable} ") 
    results = cursor.fetchall()
    return results


def checkFoodHasBeenOrdered(foodid) :
    cursor.execute(f"SELECT COUNT(*) FROM OrderItems WHERE fooditem_id = {foodid}")
    results = cursor.fetchone()[0]
    
    return results > 0

def fetchStatistics(order='DESC', category_id=None, search_term=None, date = None ):
    query = """
        SELECT f.name AS Food, c.name AS Category, IFNULL(SUM(o.quantity),0) AS Times_Ordered
        FROM FoodItems f
        LEFT JOIN Categories c ON f.category_id = c.category_id
    """
    params = []
    # date = QDate(2025, 5, 1)#, QDate(2025, 5, 6)
    # date = (QDate(2025, 5, 1), QDate(2025, 5, 6))
    if date is None :
        query += "LEFT JOIN OrderItems o ON f.fooditem_id = o.fooditem_id"
    else :
        if isinstance(date, QDate) :
            date = date.toString("yyyy-MM-dd")
            query += """LEFT JOIN (
                        SELECT ord_item.fooditem_id, ord_item.quantity
                        FROM OrderItems ord_item
                        JOIN Orders ord ON ord_item.order_id = ord.order_id
                        WHERE DATE(ord.order_datetime) = %s
                    ) o ON o.fooditem_id = f.fooditem_id
                    """
            params.append(date)
        elif isinstance(date, tuple) :
            date0 = date[0].toString("yyyy-MM-dd")
            date1 = date[1].toString("yyyy-MM-dd")
            query += """LEFT JOIN (
                        SELECT ord_item.fooditem_id, ord_item.quantity
                        FROM OrderItems ord_item
                        JOIN Orders ord ON ord_item.order_id = ord.order_id
                        WHERE DATE(ord.order_datetime) BETWEEN %s AND %s
                    ) o ON o.fooditem_id = f.fooditem_id
                    """
            params.append(date0)
            params.append(date1)

    if category_id is not None:
        query += " WHERE c.category_id = %s"
    if search_term:
        if category_id is not None:
            query += " AND f.name LIKE %s"
        else:
            query += " WHERE f.name LIKE %s"

    query += """ GROUP BY f.fooditem_id, f.name, c.name ORDER BY Times_Ordered {order}""".format(order=order)
    if category_id is not None:
        params.append(category_id)
    if search_term:
        params.append(f"%{search_term}%")
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    return results

def fetchStatisticsOnDate(date_from: QDate, date_to : QDate) :
    date_from = date_from.toString("yyyy-MM-dd")
    date_to = date_to.toString("yyyy-MM-dd")

    cursor.execute("""SELECT f_item.name food_name, 
                   IFNULL(SUM(o.quantity), 0) total_quantity
                   FROM FoodItems f_item
                   LEFT JOIN (
                       SELECT ord_item.fooditem_id, ord_item.quantity
                       FROM OrderItems ord_item
                       JOIN Orders ord ON ord_item.order_id = ord.order_id
                       WHERE DATE(ord.order_datetime) BETWEEN %s AND %s
                   ) o ON o.fooditem_id = f_item.fooditem_id
                   GROUP BY f_item.fooditem_id, f_item.name
                   ORDER BY total_quantity DESC
                   """, (date_from, date_to))
    results = cursor.fetchall()
    print(results)

# fetchStatisticsOnDate(QDate(2025, 5, 1), QDate(2025, 5, 6))

def fetchStatsOfFoodItem(foodid, DateRange) :
    DateRange = (QDate(2025, 5, 1), QDate(2025, 5, 6))
    foodid = 1
    mytuple = (foodid, DateRange[0].toString("yyyy-MM-dd"), DateRange[1].toString("yyyy-MM-dd"))
    cursor.execute("""SELECT DATE(ord.order_datetime) order_date, 
                   SUM(ord_item.quantity) total_quantity
                    FROM OrderItems ord_item
                   LEFT JOIN Orders ord ON ord_item.order_id = ord.order_id
                   WHERE ord_item.fooditem_id = %s AND ord.order_datetime BETWEEN %s AND %s
                   GROUP BY DATE(ord.order_datetime)
                   ORDER BY order_date;""", mytuple)
    results = cursor.fetchall()
    print(results)

fetchStatsOfFoodItem(1,1)

def fetchOrderHistory(date_filter=None):

    if date_filter is None:
        cursor.execute("SELECT * FROM Orders ORDER BY order_datetime DESC")

    elif isinstance(date_filter, QDate):
        date_str = date_filter.toString("yyyy-MM-dd")
        cursor.execute("SELECT * FROM Orders WHERE DATE(order_datetime) = %s ORDER BY order_datetime DESC", (date_str,))

    elif isinstance(date_filter, str):
        cursor.execute("SELECT * FROM Orders WHERE DATE(order_datetime) = %s ORDER BY order_datetime DESC", (date_filter,))

    elif isinstance(date_filter, tuple):
        start, end = date_filter
        if isinstance(start, QDate): start = start.toString("yyyy-MM-dd")
        if isinstance(end, QDate): end = end.toString("yyyy-MM-dd")
        cursor.execute("SELECT * FROM Orders WHERE DATE(order_datetime) BETWEEN %s AND %s ORDER BY order_datetime DESC", (start, end))

    results = cursor.fetchall()
    return results

def fetchOrderItemsSubtotalList(orderid) :
    cursor.execute(f"""SELECT o.order_id, f.name, oi.quantity, f.price * oi.quantity AS subtotal
                   FROM Orders AS o
                   JOIN OrderItems AS oi
                   ON o.order_id = oi.order_id
                   JOIN FoodItems AS f
                   ON oi.fooditem_id = f.fooditem_id
                   WHERE o.order_id = {orderid};
                   """)
    results = cursor.fetchall()
    return results

def fetchOrderItemsTotal(orderid) :
    cursor.execute(f"""SELECT SUM(f.price * oi.quantity) AS total
                   FROM Orders AS o
                   JOIN OrderItems AS oi
                   ON o.order_id = oi.order_id
                   JOIN FoodItems AS f
                   ON oi.fooditem_id = f.fooditem_id
                   WHERE o.order_id = {orderid};
                   """)
    results = cursor.fetchone()[0]
    return results

def fetchLatest_orderid() :
    cursor.execute(f"""SELECT order_id FROM Orders ORDER BY order_datetime DESC """)
    latestorder = cursor.fetchone()[0]
    cursor.fetchall()
    return latestorder

def fetchOrderDateTime(orderid) :
    cursor.execute(f"""SELECT order_datetime FROM Orders WHERE order_id = {orderid} """)
    latestorder = cursor.fetchone()[0]
    cursor.fetchall()
    return latestorder

# should have contained these queries into a class...

def fetchSubStrNames(substr) :
    cursor.execute(f"""SELECT f.fooditem_id, f.name, f.is_available, c.category_id, c.name 
                   FROM FoodItems AS f 
                   LEFT JOIN Categories AS c
                   ON f.category_id = c.category_id
                   WHERE f.name LIKE '%{substr}%' """)
    return cursor.fetchall()


class ProfileQueries :

    def fetchPin() :
        cursor.execute("SELECT pin FROM Profile")
        pin = cursor.fetchone()[0]
        cursor.fetchall()
        return pin

    def fetchProfileImg() :
        cursor.execute("SELECT imgfile FROM Profile")
        imgfile = cursor.fetchone()[0]
        cursor.fetchall()
        return imgfile

    def fetchProfileName() :
        cursor.execute("SELECT name FROM Profile")
        name = cursor.fetchone()[0]
        cursor.fetchall()
        return name

    def fetchDisplayName() :
        cursor.execute("SELECT is_displayname FROM Profile")
        is_displayname = cursor.fetchone()[0]
        cursor.fetchall()
        return is_displayname