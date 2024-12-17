from aiogram.types import Message  # Импортирование класса Message для работы с сообщениями в Telegram

# Хендлер для текстовой кнопки "Помощь"
async def help_button(message: Message, log_user_action):
    # Логирование действия пользователя, который нажал на кнопку "Помощь"
    log_user_action(message.from_user.id, "Нажал Помощь")
    # Отправка сообщения с инструкцией по использованию бота
    await message.answer("Вы можете заказать цветы, узнать информацию или обратиться к администратору.")

# Обёртка для передачи аргументов в хендлер помощи
def help_button_handler(log_user_action):
    async def handler(message: Message):  # Определение асинхронного обработчика
        await help_button(message, log_user_action)  # Вызов функции help_button с передачей параметров
    return handler  # Возврат обработчика, который будет использоваться в регистраторе

# Функция для регистрации хендлеров для помощи
def register_help_handlers(dp, log_user_action):
    dp.message.register(  # Регистрация хендлера для сообщений
        help_button_handler(log_user_action),  # Указание хендлера для обработки команды "Помощь"
        lambda msg: msg.text == "Помощь"  # Условие для обработки сообщений с текстом "Помощь"
    )
