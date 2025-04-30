from src.database.init_db import get_dbCursor

cursor = get_dbCursor()

def setup_pin(pin) :
    pinTuple = (pin,)
    cursor.execute("UPDATE Profile SET pin = %s WHERE profile_id = 1",pinTuple)
