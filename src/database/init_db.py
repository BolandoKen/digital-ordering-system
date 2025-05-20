import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="orderoo_db" # delete this pls, will have to refactor later
)
db.autocommit = True

mycursor = db.cursor()

def create_Database() :
    mycursor.execute("CREATE DATABASE IF NOT EXISTS orderoo_db")
    db.database = "orderoo_db"

def create_FoodItemsTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS FoodItems (
                     fooditem_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(128) NOT NULL,
                     price DECIMAL(10,2) NOT NULL,
                     imgfile VARCHAR(128) NULL,
                     is_available BOOL NOT NULL DEFAULT TRUE,
                     category_id SMALLINT NOT NULL,
                     FOREIGN KEY(category_id) REFERENCES Categories(category_id)
                     )""")

def create_CategoriesTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Categories(
                     category_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(128) NOT NULL,
                     imgfile VARCHAR(128) NULL
                     )""")

def create_OrdersTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
                     order_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     order_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                     )""")

def create_OrderItemsTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS OrderItems(
                     orderitem_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     quantity SMALLINT NOT NULL DEFAULT 1,
                     fooditem_id SMALLINT NOT NULL,
                     order_id SMALLINT NOT NULL,
                     FOREIGN KEY(fooditem_id) REFERENCES FoodItems(fooditem_id),
                     FOREIGN KEY(order_id) REFERENCES Orders(order_id)
                     )""")

def create_ProfileTable() : # independent table to keep track of account
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Profile(
                     profile_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(128) NOT NULL,
                     imgfile VARCHAR(128) NULL,
                     is_displayname BOOL NOT NULL DEFAULT TRUE,
                     pin VARCHAR(4) NULL CHECK(pin REGEXP ('^[0-9]{4}$'))
                     )""")
    
def create_ProfileRow() :
    mycursor.execute("SELECT * FROM Profile")
    results = mycursor.fetchall()
    if len(results) == 0 :
        profileTuple = ("admin",)
        mycursor.execute("""INSERT INTO Profile
                    (name)
                    VALUES (%s)
                    """, profileTuple)

def create_Tables() :
    create_CategoriesTable()
    create_OrdersTable()
    create_FoodItemsTable()
    create_OrderItemsTable()

def init_db() :
    create_Database()
    create_Tables()
    create_ProfileTable()
    create_ProfileRow()

def get_dbCursor() :
    return db.cursor()    