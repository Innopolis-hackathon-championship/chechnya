import sqlite3
import datetime
import random

conn = sqlite3.connect('menu.db')
cursor = conn.cursor()
#БД

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    user_id INTEGER,
    order_date DATE,
    food_id INTEGER,
    status INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    user_id INTEGER,
    food_id INTEGER,
    active INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    food_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    price INTEGER,
    availability TEXT,
    category TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    is_admin BOOLEAN
);
''')

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    dish TEXT,
    cost INTEGER
);
""")

#Функция добавления блюд
def add_dish(name, description, price, availability, category):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, description, price, availability, category) VALUES (?, ?, ?, ?, ?)", (name, description, price, availability, category))
    conn.commit()
    conn.close()

#Функция добавления блюд в меню
def add_dish_in_cart(user_id, dateorder, order, food_id, active):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, description, price, availability, category) VALUES (?, ?, ?, ?, ?)", (user_id, dateorder, order, food_id, active))
    conn.commit()
    conn.close()
#Получить меню из категории

def get_menu_by_category(category):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("SELECT food_id, name, description, price, availability FROM menu WHERE category = ?", (category,))
    menu_data = cursor.fetchall()
    conn.close()
    return menu_data

def get_food_by_id(food_id):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu WHERE food_id = ?", (food_id,))
    menu_data = cursor.fetchall()
    conn.close()
    return menu_data

def set_food_in_cart(food, user_id):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    food_id, user_id, dish, cost = food[0][0], user_id, food[0][1], food[0][4]
    if int(cost) < 1:
        return False
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (user_id, food_id, active) VALUES (?, ?, ?)", (user_id, food_id, 1))
    conn.commit()
    conn.close()

def set_food_in_orders(food, user_id):
    order_id = int(str(random.random())[2:14])
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    for i in food:
        food_id = i[0]
        cursor.execute("INSERT INTO orders (order_id, user_id, order_date, food_id, status) VALUES (?, ?, ?, ?, ?)", (order_id, user_id, current_date, food_id, 1))
    conn.commit()
    conn.close()

def get_foods_by_user(user_id):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("select count(r.food_id), r.*, m.name from cart r, menu m where m.food_id = r.food_id and user_id = ? and active = ? group by m.name", (user_id, 1,))
    cart = cursor.fetchall()
    conn.commit()
    conn.close()
    return cart

# Пример добавления блюда
# if input("Хотите добавить какое-нибудь блюдо в меню? ").lower() in "да":
#     name = input("Введите название блюда: ")
#     description = input("Введите описание блюда: ")
#     price = input("Введите цену: ")
#     availability = input("Есть в наличии (да/нет): ").lower()
#     if availability in "да":
#         availability = int(input("Введите кол-во блюда: "))
#     else:
#         availability = "Нет в наличии"
#     category = input("Введите к какой категории относится блюдо: ")
#     add_dish(name, description, price, availability, category)
print(get_menu_by_category("Завтрак"))
conn.commit()
conn.close()
