import logging  # Импорт модуля для логирования

from aiogram import Bot, Dispatcher  # Импорт основного функционала бота и диспетчера
from aiogram.fsm.storage.memory import MemoryStorage  # Использование памяти для хранения states-состояний

from callback import register_all_callbacks  # Импорт функции регистрации всех callback-хендлеров
from config_data.config import Config, load_config
from database.database import Database  # Импорт класса для работы с базой данных
from handlers import register_all_handlers  # Импорт функции регистрации всех хендлеров
from middlewares.logging import LoggingMiddleware, log_user_action


# Запуск бота
async def main():  # Асинхронная функция для запуска бота
    config: Config = load_config() # загрузка конфига

    db = Database(config)  # Создание экземпляра класса для работы с базой данных

    bot = Bot(token=config.tg_bot.token)  # Создание объекта бота с токеном
    dp = Dispatcher(storage=MemoryStorage())  # Создание диспетчера с использованием памяти для states
    logging.basicConfig(level=logging.INFO)  # Настройка уровня логирования (информационные сообщения)

    dp.message.middleware(LoggingMiddleware())  # Регистрация middleware для обработки сообщений

    register_all_handlers(dp, db, log_user_action, config.tg_bot.admin)  # Регистрация всех хендлеров для обработки сообщений
    register_all_callbacks(dp, log_user_action, db)  # Регистрация всех callback-хендлеров для обработки кнопок

    await dp.start_polling(bot)  # Запуск процесса polling (опрос сервера Telegram на новые события)

if __name__ == "__main__":  # Проверка, что скрипт запущен как основная программа
    import asyncio  # Импорт модуля для работы с асинхронным кодом
    asyncio.run(main())  # Запуск основного цикла работы бота
