# Middleware для логирования действий пользователя
import logging
from datetime import datetime


class LoggingMiddleware:  # Создание middleware для логирования событий
    async def __call__(self, handler, event, data):  # Асинхронный метод для перехвата событий
        user = event.from_user  # Получение данных о пользователе
        logging.info(f"User {user.id} - {user.first_name}: {getattr(event, 'text', 'No text')}")  # Логирование ID и имени пользователя
        return await handler(event, data)  # Передача события дальше в обработку


def log_user_action(user_id, action):  # Функция для логирования действий пользователя в файл
    with open("user_actions.log", "a") as file:  # Открытие файла для добавления данных
        file.write(f"{datetime.now()} - User {user_id}: {action}\n")  # Запись действия с временной меткой
