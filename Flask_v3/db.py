import sqlite3
import csv

conn = sqlite3.connect('db/HugeCrm.db', check_same_thread=False)
cursor = conn.cursor()

def make_db(): 
    cursor.execute("DROP TABLE if exists user")
    cursor.execute("DROP TABLE if exists store")
    cursor.execute("DROP TABLE if exists 'order'")
    cursor.execute("DROP TABLE if exists item")
    cursor.execute("DROP TABLE if exists order_item")

    cursor.execute("""
                CREATE TABLE user ( 
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    gender INTEGER,
                    age INTEGER,
                    birthdate TEXT,
                    address TEXT )
    """)
    cursor.execute("""
                CREATE TABLE store (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    address TEXT NOT NULL )
    """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS "order" (
                    id TEXT PRIMARY KEY,
                    ordered_at TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    store_id TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id),
                    FOREIGN KEY(store_id) REFERENCES store(id) )
    """)
    cursor.execute("""
                CREATE TABLE item (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    unit_price INTEGER NOT NULL )
    """)
    cursor.execute("""
                CREATE TABLE order_item (
                    id TEXT PRIMARY KEY,
                    order_id NOT NULL,
                    item_id NOT NULL,
                    FOREIGN KEY(order_id) REFERENCES "order"(id),
                    FOREIGN KEY(item_id) REFERENCES item(id) )
    """)

    conn.commit()

# def csv_to_db():
def user_csv_to_db():
    with open('csv/user.csv', 'r', encoding='utf-8-sig') as file:
        csv_data = csv.reader(file)
        data =[]
        for row in csv_data:
            data.append(tuple(row))
        
        cursor.executemany("INSERT INTO user(id, name, gender, age, birthdate, address) VALUES (?, ?, ?, ?, ?, ?)", data)

        conn.commit()

def store_csv_to_db():
    with open('csv/store.csv', 'r', encoding='utf-8-sig') as file:
        csv_data = csv.reader(file)
        data =[]
        for row in csv_data:
            data.append(tuple(row))

    cursor.executemany("INSERT INTO store(id,name, type, address) VALUES (?, ?, ?, ?)", data)

    conn.commit()

def item_csv_to_db():
    with open('csv/item.csv', 'r', encoding='utf-8-sig') as file:
        csv_data = csv.reader(file)
        data =[]
        for row in csv_data:
            data.append(tuple(row))

    cursor.executemany("INSERT INTO item(id, name, type, unit_price) VALUES (?, ?, ?, ?)", data)

    conn.commit()

def order_csv_to_db():
    with open('csv/order.csv', 'r', encoding='utf-8-sig') as file:
        csv_data = csv.reader(file)
        data =[]
        for row in csv_data:
            data.append(tuple(row))

    cursor.executemany("INSERT INTO 'order'(id, ordered_at, store_id, user_id) VALUES (?, ?, ?, ?)", data)

    conn.commit()

def orderitem_csv_to_db():
    with open('csv/orderitem.csv', 'r', encoding='utf-8-sig') as file:
        csv_data = csv.reader(file)
        data =[]
        for row in csv_data:
            data.append(tuple(row))

    cursor.executemany("INSERT INTO order_item(id, order_id, item_id) VALUES (?, ?, ?)", data)

    conn.commit()


make_db()
user_csv_to_db()
store_csv_to_db()
item_csv_to_db()
order_csv_to_db()
orderitem_csv_to_db()