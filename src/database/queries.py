from src.database.init_db import get_dbCursor

cursor = get_dbCursor()

def fetchCatList() :
    cursor.execute("SELECT category_id, name, imgfile FROM Categories")
    results = cursor.fetchall()
    return results

def fetchFoodUnderCatList(category_id) :
    cursor.execute(f"SELECT fooditem_id, name, price, imgfile, category_id FROM FoodItems WHERE category_id = {category_id} ")
    results = cursor.fetchall()
    return results