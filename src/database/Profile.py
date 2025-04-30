from src.database.init_db import get_dbCursor

cursor = get_dbCursor()

def setup_pin(pin) :
    pinTuple = (pin,)
    cursor.execute("UPDATE Profile SET pin = %s WHERE profile_id = 1",pinTuple)

def reset_pin() :
    pinTuple = (None,)
    cursor.execute("UPDATE Profile SET pin = %s WHERE profile_id = 1",pinTuple)

def update_name(new_name) :
    nameTuple = (new_name,)
    cursor.execute("UPDATE Profile SET name = %s WHERE profile_id = 1",nameTuple)
