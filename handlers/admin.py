from aiogram.types import Message  # Импортирование класса Message для работы с сообщениями в Telegram
from keyboards.keyboards import admin_menu  # Импортирование клавиатуры для админ панели

# Хендлер для админ панели
async def admin_panel(message: Message, log_user_action, admin_id):
    # Проверка, является ли пользователь администратором
    if message.from_user.id == admin_id:
        # Логирование успешного входа администратора в панель
        log_user_action(message.from_user.id, "Вошел в админ панель")
        # Отправка сообщения с приветствием и отображением клавиатуры админ панели
        await message.answer("Добро пожаловать в админ панель", reply_markup=admin_menu)
    else:
        # Логирование попытки несанкционированного доступа
        log_user_action(message.from_user.id, "Попытка доступа к админ панели")
        # Отправка сообщения о запрете доступа
        await message.answer("У вас нет доступа к админ панели.")

# Обёртка для передачи аргументов в админ-хендлер
def admin_panel_handler(log_user_action, admin_id):
    async def handler(message: Message):  # Определение асинхронного обработчика
        await admin_panel(message, log_user_action, admin_id)  # Вызов функции admin_panel с передачей параметров
    return handler  # Возврат обработчика, который будет использоваться в регистраторе

# Функция для регистрации хендлеров для админ панели
def register_admin_handlers(dp, log_user_action, admin_id):
    dp.message.register(  # Регистрация хендлера для сообщений
        admin_panel_handler(log_user_action, admin_id),  # Указание хендлера для обработки команды "Админ панель"
        lambda msg: msg.text == "Админ панель"  # Условие для обработки сообщений с текстом "Админ панель"
    )
