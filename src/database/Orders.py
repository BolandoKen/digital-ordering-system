# from src.database.init_db import get_dbCursor
from init_db import get_dbCursor

cursor = get_dbCursor()

mockOrderItemTupleArr = [(4, 1), (1, 2)]

def addOrder(orderItemTupleArr) :
    cursor.execute("INSERT INTO Orders () VALUES ()")

    # add all orderItemTuple in the arr to OrderItemsTable
    cursor.execute("SELECT order_id FROM Orders ORDER BY order_datetime DESC")
    recent_order_id = cursor.fetchone()

    for orderItemTuple in orderItemTupleArr :
        new_orderItemTuple = orderItemTuple + (recent_order_id)
        cursor.execute("""INSERT INTO OrderItems
                       (quantity, fooditem_id, order_id)
                       VALUES (%s, %s, %s)
                       """, new_orderItemTuple)

