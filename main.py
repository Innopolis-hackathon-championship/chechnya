import telebot
from telebot import types
import os
from dotenv import load_dotenv
from data import get_menu_by_category, add_dish, get_food_by_id, set_food_in_cart, get_foods_by_user, set_food_in_orders
from functions import keyboard_generate, get_name_from_category
import sqlite3

conn = sqlite3.connect('menu.db')

cursor = conn.cursor()
rows = cursor.fetchall()

load_dotenv()

TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

# markup_for_start = types.InlineKeyboardMarkup()
# menu_markup = types.InlineKeyboardButton("Меню", callback_data="menu_markup")
# markup_for_start.add(menu_markup)

markup_for_start_admin = types.InlineKeyboardMarkup()
menu_markup_admin = types.InlineKeyboardButton("Меню", callback_data="menu_markup")
menu_change_markup = types.InlineKeyboardButton("Изменить меню", callback_data="menu_change")
markup_for_start_admin.add(menu_markup_admin, menu_change_markup)

keyboard = types.InlineKeyboardMarkup()
breakfast_button = types.InlineKeyboardButton("Завтрак", callback_data="breakfast_button")
lunch_button = types.InlineKeyboardButton("Обед", callback_data="lunch_button")
diner_button = types.InlineKeyboardButton("Ужин", callback_data="diner_button")
drinks_button = types.InlineKeyboardButton("Напитки", callback_data="drinks_button")
dessert_button = types.InlineKeyboardButton("Десерты", callback_data="dessert_button")
snacks_button = types.InlineKeyboardButton("Снеки", callback_data="snacks_button")
keyboard.add(breakfast_button, lunch_button, diner_button, drinks_button, dessert_button, snacks_button)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бот-буфет!", reply_markup=markup_for_start_admin)
    # user_id = message.from_user.id
    # username = message.from_user.username

    # # Проверяем, есть ли пользователь в базе данных
    # cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    # existing_user = cursor.fetchone()
    # if not existing_user:
    #     # Если пользователь отсутствует в базе данных, добавляем его как обычного пользователя
    #     cursor.execute("INSERT INTO users (user_id, username, is_admin) VALUES (?, ?, ?)", (user_id, username, False))
    #     conn.commit()

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Для того чтобы вызвать меню напишите команду /menu")

@bot.message_handler(commands=['cart'])
def cart(message):
    list_cart = get_foods_by_user(message.chat.id)
    new_menu = ""
    for i, val in enumerate(list_cart):
        val = f"{val[6]} - {val[0]} шт. \n"
        new_menu += val
    bot.send_message(message.chat.id, new_menu)

@bot.message_handler(commands=['menu'])
def menu(message):
    # if user_id == admin:
    # else:
    bot.send_message(message.chat.id, "Выберите категорию меню", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data[0:4] == "food":
        food_id = call.data[4:6]
        user_id = call.from_user.id
        food = get_food_by_id(food_id)
        set_food_in_cart(food, user_id) #Добавление в корзину
        keyboard_cart = types.InlineKeyboardMarkup()
        cart = types.InlineKeyboardButton("КОРЗИНА", callback_data="cart")
        order = types.InlineKeyboardButton("ОФОРМИТЬ ЗАКАЗ", callback_data="create_order")
        menu = types.InlineKeyboardButton("НАЗАД В МЕНЮ", callback_data="menu")
        keyboard_cart.add(cart, order, menu)
        bot.send_message(call.message.chat.id, f"Добавлено в корзину {food[0][1]} - {food[0][3]}", reply_markup=keyboard_cart)
        print('Добавлено')

    if call.data == "cart": #Повторяет ровно тоже что и def cart()
        list_cart = get_foods_by_user(call.message.chat.id)
        new_menu = ""
        for i, val in enumerate(list_cart):
            val = f"{val[6]} - {val[0]} шт. \n"
            new_menu += val
        bot.send_message(call.message.chat.id, new_menu)

    if call.data == "create_order":
        list_cart = get_foods_by_user(call.message.chat.id)
        set_food_in_orders(list_cart, call.message.chat.id)


    if call.data == "breakfast_button":
        zac = get_menu_by_category("Завтрак")
        breakfast_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=breakfast_keyboard)
    elif call.data == "lunch_button":
        zac = get_menu_by_category("Обед")
        lunch_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, get_name_from_category(zac) + "\n" + "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=lunch_keyboard)
    elif call.data == "diner_button":
        zac = get_menu_by_category("Ужин")
        diner_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, get_name_from_category(zac) + "\n" + "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=diner_keyboard)
    elif call.data == "drinks_button":
        zac = get_menu_by_category("Напитки")
        drinks_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, get_name_from_category(zac) + "\n" + "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=drinks_keyboard)
    elif call.data == "dessert_button":
        zac = get_menu_by_category("Десерты")
        dessert_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, get_name_from_category(zac) + "\n" + "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=dessert_keyboard)
    elif call.data == "snacks_button":
        zac = get_menu_by_category("Снеки")
        snacks_keyboard = keyboard_generate(zac)
        bot.send_message(call.message.chat.id, get_name_from_category(zac) + "\n" + "Чтобы добавить в корзину выберите блюдо снизу по кнопке: ", reply_markup=snacks_keyboard)
    elif call.data == "menu_markup":
        bot.send_message(call.message.chat.id, "Выберите категорию меню", reply_markup=keyboard)
    # elif call.data == "menu_change":
    #     name = input("Введите название блюда: ")
    #     description = input("Введите описание блюда: ")
    #     price = input("Введите цену: ")
    #     availability = input("Есть в наличии (да/нет): ").lower()
    #     if availability in "да":
    #              availability = int(input("Введите кол-во блюда: "))
    #     else:
    #              availability = "Нет в наличии"
    #     category = input("Введите к какой категории относится блюдо: ")
    #     bot.send_message(call.message.chat.id, add_dish())
@bot.message_handler(func=lambda call: call.lower() == "menu_change")
def menu_change(message):
    bot.send_message(message.chat.id, "Введите название блюда:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите описание блюда:")
    bot.register_next_step_handler(message, get_description, name)

def get_description(message, name):
    description = message.text
    bot.send_message(message.chat.id, "Введите цену:")
    bot.register_next_step_handler(message, get_price, name, description)

def get_price(message, name, description):
    price = message.text
    bot.send_message(message.chat.id, "Есть в наличии (да/нет):")
    bot.register_next_step_handler(message, get_availability, name, description, price)

def get_availability(message, name, description, price):
    availability_text = message.text.lower()
    if availability_text == "да":
        availability = True
        bot.send_message(message.chat.id, "Введите количество блюда:")
        bot.register_next_step_handler(message, get_quantity, name, description, price, availability)
    else:
        availability = False
        quantity = "Нет в наличии"
        category = input("Введите к какой категории относится блюдо:")
        add_dish(name, description, price, availability, category)
        bot.send_message(message.chat.id, "Блюдо успешно добавлено!")

def get_quantity(message, name, description, price, availability):
    quantity = message.text
    bot.send_message(message.chat.id, "Введите к какой категории относится блюдо:")
    bot.register_next_step_handler(message, get_category, name, description, price, availability, quantity)

def get_category(message, name, description, price, availability, quantity):
    category = message.text
    add_dish(name, description, price, availability, category, quantity)
    bot.send_message(message.chat.id, "Блюдо успешно добавлено!")






bot.polling(non_stop=True)
