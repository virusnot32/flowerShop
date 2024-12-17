from aiogram.types import Message, CallbackQuery  # Импортирование классов для обработки сообщений и callback-запросов
from aiogram.filters import StateFilter  # Импортирование фильтра для работы с состояниями
from aiogram.fsm.context import FSMContext  # Импортирование контекста для работы с состоянием машины состояний
from states.states import OrderState  # Импортирование состояний для процесса заказа
from keyboards.keyboards import confirmation_menu  # Импортирование клавиатуры для подтверждения заказа

# Основные хендлеры

# Хендлер для выбора цветка
async def flower_selected(callback: CallbackQuery, state: FSMContext, log_user_action, db):
    flower = callback.data.split("_")[1]  # Извлечение выбранного цветка из callback_data
    await state.update_data(selected_flower=flower)  # Сохранение выбранного цветка в состояние
    log_user_action(callback.from_user.id, f"Выбрал цветок: {flower}")  # Логирование выбора цветка
    await callback.message.answer(f"Вы выбрали {flower}. Укажите количество:")  # Отправка сообщения с просьбой ввести количество
    await state.set_state(OrderState.enter_quantity)  # Установка состояния для ввода количества

# Хендлер для ввода количества
async def enter_quantity(message: Message, state: FSMContext, log_user_action):
    quantity = int(message.text)  # Преобразование введенного текста в количество
    if quantity <= 0:  # Проверка, что количество больше нуля
        await message.answer("Введите число больше нуля.")  # Сообщение, если количество неверно
        return
    await state.update_data(quantity=quantity)  # Сохранение введенного количества в состояние
    data = await state.get_data()  # Получение данных состояния
    flower = data["selected_flower"]  # Извлечение выбранного цветка из состояния
    log_user_action(message.from_user.id, f"Указал количество: {quantity}")  # Логирование указанного количества
    await message.answer(f"Вы хотите заказать {quantity} шт. {flower}. Подтвердите заказ.", reply_markup=confirmation_menu)  # Запрос подтверждения заказа
    await state.set_state(OrderState.confirm_order)  # Установка состояния для подтверждения заказа

# Хендлер для подтверждения заказа
async def confirm_order(callback: CallbackQuery, state: FSMContext, log_user_action, db):
    data = await state.get_data()  # Получение данных состояния
    flower = data["selected_flower"]  # Извлечение выбранного цветка из состояния
    quantity = data["quantity"]  # Извлечение количества из состояния
    db.add_order(callback.from_user.id, flower, quantity)  # Добавление заказа в базу данных
    log_user_action(callback.from_user.id, f"Подтвердил заказ: {quantity} шт. {flower}")  # Логирование подтверждения заказа
    await callback.message.answer(f"Ваш заказ подтвержден: {quantity} шт. {flower}. Спасибо за покупку!")  # Сообщение о подтверждении заказа
    await state.clear()  # Очистка состояния

# Хендлер для отмены заказа
async def cancel_order(callback: CallbackQuery, state: FSMContext, log_user_action):
    log_user_action(callback.from_user.id, "Отменил заказ")  # Логирование отмены заказа
    await callback.message.answer("Ваш заказ был отменен.")  # Сообщение об отмене заказа
    await state.clear()  # Очистка состояния

# Регистрация callback-хендлеров

# Функция для регистрации всех callback-хендлеров
def register_users_callbacks(dp, log_user_action, db):
    @dp.callback_query(lambda cb: cb.data.startswith("flower_"))  # Хендлер для выбора цветка
    async def flower_selected_handler(callback: CallbackQuery, state: FSMContext):
        await flower_selected(callback, state, log_user_action, db)  # Вызов хендлера выбора цветка

    @dp.message(StateFilter(OrderState.enter_quantity))  # Хендлер для ввода количества
    async def enter_quantity_handler(message: Message, state: FSMContext):
        await enter_quantity(message, state, log_user_action)  # Вызов хендлера ввода количества

    @dp.callback_query(lambda cb: cb.data == "confirm_order")  # Хендлер для подтверждения заказа
    async def confirm_order_handler(callback: CallbackQuery, state: FSMContext):
        await confirm_order(callback, state, log_user_action, db)  # Вызов хендлера подтверждения заказа

    @dp.callback_query(lambda cb: cb.data == "cancel_order")  # Хендлер для отмены заказа
    async def cancel_order_handler(callback: CallbackQuery, state: FSMContext):
        await cancel_order(callback, state, log_user_action)  # Вызов хендлера отмены заказа
