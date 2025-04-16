from src.database.init_db import get_dbCursor
from src.database.queries import checkFoodHasBeenOrdered
from src.utils.PixMap import deleteImageOfFood

cursor = get_dbCursor()

def addFoodItem(foodTuple, hasImg) :
    cursor.execute("""INSERT INTO FoodItems
                   ( name, price, imgfile, category_id)
                   VALUES (%s,  %s, %s, %s)
                   """, foodTuple)
    if hasImg is False :
        return None
    lastrowid = cursor.lastrowid
    imgfileName = f"{lastrowid}.png"
    cursor.execute("UPDATE FoodItems SET imgfile=%s WHERE fooditem_id = %s", (imgfileName, lastrowid))
    return imgfileName

def editFoodItem(foodTuple, hasImg) :
    _,_,_,_,fooditem_id = foodTuple
    cursor.execute("""UPDATE FoodItems
                   SET name = %s, 
                   price = %s,
                   imgfile = %s,
                   category_id = %s
                   WHERE fooditem_id = %s
                   """, foodTuple)
    if hasImg is False :
        return None
    imgfileName = f"{fooditem_id}.png"
    cursor.execute("UPDATE FoodItems SET imgfile=%s WHERE fooditem_id = %s", (imgfileName, fooditem_id))
    return imgfileName

def deleteFoodItem(foodid) :
    if checkFoodHasBeenOrdered(foodid) :
        cursor.execute("UPDATE FoodItems SET is_available = %s WHERE fooditem_id = %s",( False, foodid))
        print('food has previously been ordered, will soft delete!')
    else : 
        print('deleted', foodid)
        deleteImageOfFood(foodid)
        cursor.execute(f"DELETE FROM FoodItems WHERE fooditem_id = {foodid}")
        
    # to do: listing for unavailable items

def reviveFoodItem(foodid) :
    cursor.execute("UPDATE FoodItems SET is_available = %s WHERE fooditem_id = %s", (True, foodid))
    