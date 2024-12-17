from .start import register_start_handlers  # Импортирование функции для регистрации хендлеров команды /start
from .help import register_help_handlers  # Импортирование функции для регистрации хендлеров помощи
from .admin import register_admin_handlers  # Импортирование функции для регистрации хендлеров админ панели
from .order_flowers import register_order_flowers_handlers  # Импортирование функции для регистрации хендлеров заказа цветов

# Функция для регистрации всех хендлеров
def register_all_handlers(dp, db, log_user_action, admin_id):
    # Регистрация хендлеров для команды /start
    register_start_handlers(dp, db, log_user_action)
    # Регистрация хендлеров для кнопки "Помощь"
    register_help_handlers(dp, log_user_action)
    # Регистрация хендлеров для админ панели с проверкой на admin_id
    register_admin_handlers(dp, log_user_action, admin_id)
    # Регистрация хендлеров для заказа цветов
    register_order_flowers_handlers(dp, log_user_action)
