from aiogram.types import Message, CallbackQuery  # Импортирование классов для обработки сообщений и callback-запросов
from aiogram.filters import StateFilter  # Импортирование фильтра для работы с состояниями
from aiogram.fsm.context import FSMContext  # Импортирование контекста для работы с состоянием машины состояний

from states.states import AdminState  # Импортирование состояний для админ-панели

# Хендлеры для кнопок админ-панели
async def admin_actions(callback: CallbackQuery, state: FSMContext, db, log_user_action):
    action = callback.data  # Получение действия, выбранного пользователем

    if action == "admin_stats":  # Если запрос на статистику
        users_count, orders_count = db.get_statistics()  # Получаем статистику
        log_user_action(callback.from_user.id, "Запросил статистику")  # Логирование запроса статистики
        await callback.message.answer(f"Всего пользователей: {users_count}\nВсего заказов: {orders_count}")  # Отправка статистики

    elif action == "add_flower":  # Если выбрана опция добавления цветка
        log_user_action(callback.from_user.id, "Начал добавление цветка")  # Логирование начала добавления
        await callback.message.answer("Введите название цветка для добавления:")  # Запрос на ввод названия цветка
        await state.set_state(AdminState.add_flower)  # Установка состояния для добавления цветка

    elif action == "delete_flower":  # Если выбрана опция удаления цветка
        log_user_action(callback.from_user.id, "Начал удаление цветка")  # Логирование начала удаления
        await callback.message.answer("Введите название цветка для удаления:")  # Запрос на ввод названия цветка для удаления
        await state.set_state(AdminState.delete_flower)  # Установка состояния для удаления цветка

    elif action == "delete_user":  # Если выбрана опция удаления пользователя
        log_user_action(callback.from_user.id, "Начал удаление пользователя")  # Логирование начала удаления пользователя
        await callback.message.answer("Введите ID пользователя для удаления:")  # Запрос на ввод ID пользователя для удаления
        await state.set_state(AdminState.delete_user)  # Установка состояния для удаления пользователя

    elif action == "delete_order":  # Если выбрана опция удаления заказа
        log_user_action(callback.from_user.id, "Начал удаление заказа")  # Логирование начала удаления заказа
        await callback.message.answer("Введите ID заказа для удаления:")  # Запрос на ввод ID заказа для удаления
        await state.set_state(AdminState.delete_order)  # Установка состояния для удаления заказа


# Хендлеры для обработки операций с цветками, пользователями и заказами
async def process_add_flower(message: Message, state: FSMContext, db, log_user_action):
    flower_name = message.text  # Получение названия цветка из текста сообщения
    db.add_flower(flower_name)  # Добавление цветка в базу данных
    log_user_action(message.from_user.id, f"Добавил цветок: {flower_name}")  # Логирование добавления цветка
    await message.answer(f"Цветок {flower_name} успешно добавлен.")  # Отправка сообщения об успешном добавлении
    await state.clear()  # Очистка состояния

async def process_delete_flower(message: Message, state: FSMContext, db, log_user_action):
    flower_name = message.text  # Получение названия цветка из текста сообщения
    db.delete_flower(flower_name)  # Удаление цветка из базы данных
    log_user_action(message.from_user.id, f"Удалил цветок: {flower_name}")  # Логирование удаления цветка
    await message.answer(f"Цветок {flower_name} успешно удален.")  # Отправка сообщения об успешном удалении
    await state.clear()  # Очистка состояния

async def process_delete_user(message: Message, state: FSMContext, db, log_user_action):
    user_id = message.text  # Получение ID пользователя из текста сообщения
    db.delete_user(int(user_id))  # Удаление пользователя из базы данных
    log_user_action(message.from_user.id, f"Удалил пользователя: {user_id}")  # Логирование удаления пользователя
    await message.answer(f"Пользователь с ID {user_id} успешно удален.")  # Отправка сообщения об успешном удалении
    await state.clear()  # Очистка состояния

async def process_delete_order(message: Message, state: FSMContext, db, log_user_action):
    order_id = message.text  # Получение ID заказа из текста сообщения
    db.delete_order(int(order_id))  # Удаление заказа из базы данных
    log_user_action(message.from_user.id, f"Удалил заказ: {order_id}")  # Логирование удаления заказа
    await message.answer(f"Заказ с ID {order_id} успешно удален.")  # Отправка сообщения об успешном удалении
    await state.clear()  # Очистка состояния


# Функция для регистрации callback-хендлеров
def register_admin_callbacks(dp, log_user_action, db):
    @dp.callback_query(lambda cb: cb.data in ["admin_stats", "add_flower", "delete_flower", "delete_user", "delete_order"])
    async def admin_actions_handler(callback: CallbackQuery, state: FSMContext):
        await admin_actions(callback, state, db, log_user_action)

    @dp.message(StateFilter(AdminState.add_flower))
    async def process_add_flower_handler(message: Message, state: FSMContext):
        await process_add_flower(message, state, db, log_user_action)

    @dp.message(StateFilter(AdminState.delete_flower))
    async def process_delete_flower_handler(message: Message, state: FSMContext):
        await process_delete_flower(message, state, db, log_user_action)

    @dp.message(StateFilter(AdminState.delete_user))
    async def process_delete_user_handler(message: Message, state: FSMContext):
        await process_delete_user(message, state, db, log_user_action)

    @dp.message(StateFilter(AdminState.delete_order))
    async def process_delete_order_handler(message: Message, state: FSMContext):
        await process_delete_order(message, state, db, log_user_action)
