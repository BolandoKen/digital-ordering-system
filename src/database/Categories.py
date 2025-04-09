from src.database.init_db import get_dbCursor
from src.database.queries import fetchFoodUnderCatList
from src.utils.PubSub import pubsub
cursor = get_dbCursor()

def addCategory(catTuple, hasImg) :
    cursor.execute("""INSERT INTO Categories 
                   (name, imgfile)
                   VALUES (%s, %s)
                   """, catTuple)
    if hasImg is False : # checks only if it has an img apppended
        return None
    lastrowid = cursor.lastrowid
    imgfileName = f"{lastrowid}.png" # assign a name to the img, and edit to recent entry
    cursor.execute("UPDATE Categories SET imgfile = %s WHERE category_id = %s", (imgfileName,lastrowid))
    return imgfileName # return the name, to save to assets renamed

def editCategory(catTuple, hasImg) :
    _,_, category_id = catTuple
    cursor.execute("""UPDATE Categories
                   SET name = %s, imgfile = %s
                   WHERE category_id = %s                
                   """, catTuple)
    if hasImg is False : # checks only if it has an img apppended
        return None
    imgfileName = f"{category_id}.png" # assign a name to the img, and edit to recent entry
    cursor.execute("UPDATE Categories SET imgfile = %s WHERE category_id = %s", (imgfileName,category_id))
    return imgfileName

def deleteCategory(cat) :
    foodUnderCatCount = len(fetchFoodUnderCatList(cat))
    if foodUnderCatCount <=0 :
        cursor.execute(f"DELETE FROM Categories WHERE category_id = {cat}")
        pubsub.publish("updateCategory") 
    else :
        print('cant delete category! has ', foodUnderCatCount, ' food items under it.') 
    # if has any items at all, do not hard delete
    # if none, hard delete

    # category listing note: if categories has at least one available item it is considered not empty, otherwise empty  

    # to do : listing for inactive/empty categories, 
    # on update check item deletion/transfer if category in question is empty

