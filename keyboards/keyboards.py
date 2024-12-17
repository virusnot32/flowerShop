# Импортирование необходимых классов для работы с клавишами и кнопками в Telegram боте
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # Импортирование классов для создания клавиатур и кнопок
from aiogram.utils.keyboard import ReplyKeyboardBuilder  # Импортирование класса для создания ответных клавиатур

# Создание клавиатуры для главного меню с помощью ReplyKeyboardBuilder
main_menu = ReplyKeyboardBuilder()  # Инициализация объекта для создания клавиатуры
main_menu.button(text="Заказать цветы")  # Добавление кнопки "Заказать цветы"
main_menu.button(text="Помощь")  # Добавление кнопки "Помощь"
main_menu.button(text="Админ панель")  # Добавление кнопки "Админ панель"A
main_menu.adjust(1)  # Настройка клавиатуры, чтобы кнопки располагались в одном столбце

# Создание клавиатуры для админского меню с помощью InlineKeyboardMarkup
admin_menu = InlineKeyboardMarkup(inline_keyboard=[  # Инициализация клавиатуры с кнопками
    [InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],  # Кнопка "Статистика", при нажатии отправляется callback_data "admin_stats"
    [InlineKeyboardButton(text="Добавить цветок", callback_data="add_flower")],  # Кнопка "Добавить цветок"
    [InlineKeyboardButton(text="Удалить цветок", callback_data="delete_flower")],  # Кнопка "Удалить цветок"
    [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],  # Кнопка "Удалить пользователя"
    [InlineKeyboardButton(text="Удалить заказ", callback_data="delete_order")]  # Кнопка "Удалить заказ"
])

# Создание клавиатуры для выбора цветов с помощью InlineKeyboardMarkup
flowers_menu = InlineKeyboardMarkup(inline_keyboard=[  # Инициализация клавиатуры с кнопками
    [InlineKeyboardButton(text="Розы", callback_data="flower_rose")],  # Кнопка для выбора роз
    [InlineKeyboardButton(text="Тюльпаны", callback_data="flower_tulip")],  # Кнопка для выбора тюльпанов
    [InlineKeyboardButton(text="Орхидеи", callback_data="flower_orchid")]  # Кнопка для выбора орхидей
])

# Создание клавиатуры для подтверждения или отмены заказа с помощью InlineKeyboardMarkup
confirmation_menu = InlineKeyboardMarkup(inline_keyboard=[  # Инициализация клавиатуры с кнопками
    [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_order")],  # Кнопка "Подтвердить" для подтверждения заказа
    [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]  # Кнопка "Отменить" для отмены заказа
])
