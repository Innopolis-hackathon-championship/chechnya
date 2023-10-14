from telebot import types

#Функиция генерация клавиатуры
def keyboard_generate(menu):
    print('Генерация клавиатуры')
    keyboard = types.InlineKeyboardMarkup()
    #breakfast_button = types.InlineKeyboardButton("Завтрак", callback_data="breakfast_button")
    for index, food in enumerate(menu):
        print(food[0])
        keyboard.add(types.InlineKeyboardButton(food[1] + " - " + str(food[3]), callback_data=f"food{food[0]}"))
        print(f"food{food[0]}")
    return keyboard

def get_name_from_category(menu):
    # menu = [('Омлет', 'Яйцо и овощи', '120 рублей', '100'), ('Каша Овсяная', 'Каша из Овсянной крупы', '200 рублей ', '100')]
    new_menu = ""
    for i, val in enumerate(menu):
        val = f"{val[1]}   |  "
        new_menu += val
    new_menu = new_menu[:-3] 
    return new_menu


