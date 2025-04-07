from src.database.init_db import get_dbCursor
from src.database.queries import checkFoodHasBeenOrdered

cursor = get_dbCursor()

def addFoodItem(foodTuple) :
    cursor.execute("""INSERT INTO FoodItems
                   ( name, price, imgfile, category_id)
                   VALUES (%s,  %s, %s, %s)
                   """, foodTuple)

def editFoodItem(foodTuple) :
    cursor.execute("""UPDATE FoodItems
                   SET name = %s, 
                   price = %s,
                   imgfile = %s,
                   category_id = %s
                   WHERE fooditem_id = %s
                   """, foodTuple)

def deleteFoodItem(foodid) :
    if checkFoodHasBeenOrdered(foodid) :
        cursor.execute("UPDATE FoodItems SET is_available = %s WHERE fooditem_id = %s",( False, foodid))
        print('food has previously been ordered, will soft delete!')
    else : 
        print('deleted', foodid)
        cursor.execute(f"DELETE FROM FoodItems WHERE fooditem_id = {foodid}")
        
    # to do: listing for unavailable items