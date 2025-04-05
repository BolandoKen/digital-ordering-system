from src.database.init_db import get_dbCursor

cursor = get_dbCursor()

def addCategory(catTuple) :
    cursor.execute("""INSERT INTO Categories 
                   (name, imgfile)
                   VALUES (%s, %s)
                   """, catTuple)

def editCategory(catTuple) :
    cursor.execute("""UPDATE Categories
                   SET name = %s, imgfile = %s
                   WHERE category_id = %s                
                   """, catTuple)

def deleteCategory(cat) :
    print('wait') 
    # if has any items at all, do not hard delete
    # if none, hard delete

    # category listing note: if categories has at least one available item it is considered not empty, otherwise empty  

