from aiogram.types import Message  # Импортирование класса Message для работы с сообщениями в Telegram
from aiogram.fsm.context import FSMContext  # Импортирование класса FSMContext для работы с состояниями в states
from states.states import OrderState  # Импортирование состояний заказа цветов из модуля states
from keyboards.keyboards import flowers_menu  # Импортирование клавиатуры с выбором цветов

# Хендлер для команды "Заказать цветы"
async def order_flowers(message: Message, state: FSMContext, log_user_action):
    # Логирование действия пользователя, который начал заказ цветов
    log_user_action(message.from_user.id, "Начал заказ цветов")
    # Отправка сообщения с просьбой выбрать цветы и отображение клавиатуры с цветами
    await message.answer("Выберите цветы:", reply_markup=flowers_menu)
    # Установка состояния для выбора цветка в states
    await state.set_state(OrderState.choose_flower)

# Обёртка для передачи аргументов в хендлер заказа цветов
def order_flowers_handler(log_user_action):
    async def handler(message: Message, state: FSMContext):  # Определение асинхронного обработчика
        await order_flowers(message, state, log_user_action)  # Вызов функции order_flowers с передачей параметров
    return handler  # Возврат обработчика, который будет использоваться в регистраторе

# Функция для регистрации хендлеров для заказа цветов
def register_order_flowers_handlers(dp, log_user_action):
    dp.message.register(  # Регистрация хендлера для сообщений
        order_flowers_handler(log_user_action),  # Указание хендлера для обработки команды "Заказать цветы"
        lambda msg: msg.text == "Заказать цветы"  # Условие для обработки сообщений с текстом "Заказать цветы"
    )
