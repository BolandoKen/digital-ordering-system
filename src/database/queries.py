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

def fetchStatistics(order='DESC', category_id=None):
    if category_id is not None:
        cursor.execute(f"""
            SELECT f.name AS Food, c.name AS Category, IFNULL(SUM(o.quantity),0) AS Times_Ordered
            FROM FoodItems f
            LEFT JOIN Categories c ON f.category_id = c.category_id
            LEFT JOIN OrderItems o ON f.fooditem_id = o.fooditem_id
            WHERE c.category_id = %s
            GROUP BY f.fooditem_id, f.name, c.name
            ORDER BY Times_Ordered {order}
        """, (category_id,))
    else:
        cursor.execute(f"""
            SELECT f.name AS Food, c.name AS Category, IFNULL(SUM(o.quantity),0) AS Times_Ordered
            FROM FoodItems f
            LEFT JOIN Categories c ON f.category_id = c.category_id
            LEFT JOIN OrderItems o ON f.fooditem_id = o.fooditem_id
            GROUP BY f.fooditem_id, f.name, c.name
            ORDER BY Times_Ordered {order}
        """)
        
    results = cursor.fetchall()
    return results

def fetchOrderHistory(date_filter=None):
    print(f"Called fetchOrderHistory with date_filter: {date_filter}")

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
    print(results)
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