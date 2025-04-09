from src.database.init_db import get_dbCursor
import traceback

cursor = get_dbCursor()

def fetchCatList(pageName) :
    if pageName == "admin" :
        cursor.execute("SELECT category_id, name, imgfile FROM Categories")
    elif pageName == "customer" :
        cursor.execute("""SELECT c.category_id, c.name, c.imgfile
                    FROM Categories AS c
                    LEFT JOIN FoodItems AS f
                    ON c.category_id = f.category_id
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
    pass


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

def fetchStatistics(order='DESC') :
    #chatgpt gikan ang pagkuha sa times ordered, nangutana langko unsaon pagkuha sa sum sa tanan quantity gikan sa orderitems
    cursor.execute(f"""SELECT f.name AS Food, c.name AS Category, IFNULL(SUM(o.quantity),0) AS Times_Ordered
                   FROM FoodItems f
                   LEFT JOIN Categories c ON f.category_id = c.category_id
                   LEFT JOIN OrderItems o ON f.fooditem_id = o.fooditem_id
                   GROUP BY f.fooditem_id, f.name, c.name
                   ORDER BY Times_Ordered {order}
                   """)
    results = cursor.fetchall()
    return results

def fetchOrderHistory() :
    cursor.execute(f"""SELECT * FROM Orders ORDER BY order_datetime DESC """)
    results = cursor.fetchall()
    return results
