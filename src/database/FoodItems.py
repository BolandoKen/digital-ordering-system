from src.database.init_db import get_dbCursor

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

def deleteFoodItem(cat) :
    print('wait') 
    # do later
 