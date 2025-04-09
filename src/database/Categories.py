from src.database.init_db import get_dbCursor
from src.database.queries import fetchFoodUnderCatList

cursor = get_dbCursor()

def addCategory(catTuple, hasImg) :
    _,imgfile = catTuple
    cursor.execute("""INSERT INTO Categories 
                   (name, imgfile)
                   VALUES (%s, %s)
                   """, catTuple)
    if hasImg is False :
        return None
    lastrowid = cursor.lastrowid
    imgfileName = f"{lastrowid}.png"
    cursor.execute("UPDATE Categories SET imgfile = %s WHERE category_id = %s", (imgfileName,lastrowid))
    return imgfileName

def editCategory(catTuple) :
    cursor.execute("""UPDATE Categories
                   SET name = %s, imgfile = %s
                   WHERE category_id = %s                
                   """, catTuple)

def deleteCategory(cat) :
    foodUnderCatCount = len(fetchFoodUnderCatList(cat))
    if foodUnderCatCount <=0 :
        cursor.execute(f"DELETE FROM Categories WHERE category_id = {cat}")
    else :
        print('cant delete category! has ', foodUnderCatCount, ' food items under it.') 
    # if has any items at all, do not hard delete
    # if none, hard delete

    # category listing note: if categories has at least one available item it is considered not empty, otherwise empty  

    # to do : listing for inactive/empty categories, 
    # on update check item deletion/transfer if category in question is empty

