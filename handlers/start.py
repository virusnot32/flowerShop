# Хендлер для команды /start

from aiogram.types import Message  # Импортирование класса Message для работы с сообщениями в Telegram
from aiogram.filters import Command  # Импортирование фильтра для команд
from keyboards.keyboards import main_menu  # Импортирование главной клавиатуры (main_menu) из модуля keyboards

# Асинхронная функция для обработки команды /start
async def start_command(message: Message, db, log_user_action):
    # Добавление пользователя в базу данных (db) с его id, именем и фамилией
    db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    # Логирование действия пользователя, который запустил команду /start
    log_user_action(message.from_user.id, "Запустил /start")
    # Отправка приветственного сообщения и отображение главного меню
    await message.answer("Добро пожаловать в магазин цветов!", reply_markup=main_menu.as_markup())

# Регистрация хендлера для команды /start в диспетчере событий (dp)
def register_start_handlers(dp, db, log_user_action):
    dp.message.register(start_command_handler(db, log_user_action), Command(commands=["start"]))  # Регистрация хендлера для команды /start

# Функция-обёртка для передачи аргументов в хендлер
def start_command_handler(db, log_user_action):
    async def handler(message: Message):  # Определение асинхронной функции handler для обработки сообщения
        await start_command(message, db, log_user_action)  # Вызов функции start_command с передачей параметров
    return handler  # Возвращение обработчика, который будет использоваться в регистраторе
