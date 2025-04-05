import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="orderoo_db" # delete this pls, will have to refactor later
)

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
                     is_available BOOL NOT NULL DEFAULT FALSE,
                     category_id SMALLINT NOT NULL,
                     FOREIGN KEY(category_id) REFERENCES Categories(category_id)
                     )""")

def create_CategoriesTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Categories(
                     category_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(128) NOT NULL
                     )""")

def create_OrdersTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
                     order_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     total_cost DECIMAL(10,2) NOT NULL,
                     order_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                     )""")

def create_OrderItemsTable() :
    mycursor.execute("""CREATE TABLE IF NOT EXISTS OrderItems(
                     orderitem_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                     quantity SMALLINT NOT NULL DEFAULT 1,
                     subtotal DECIMAL(10,2) NOT NULL,
                     fooditem_id SMALLINT NOT NULL,
                     order_id SMALLINT NOT NULL,
                     FOREIGN KEY(fooditem_id) REFERENCES FoodItems(fooditem_id),
                     FOREIGN KEY(order_id) REFERENCES Orders(order_id)
                     )""")

def create_Tables() :
    create_CategoriesTable()
    create_OrdersTable()
    create_FoodItemsTable()
    create_OrderItemsTable()

def init_db() :
    create_Database()
    create_Tables()

def get_dbCursor() :
    return db.cursor()    