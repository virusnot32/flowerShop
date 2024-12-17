from .callback_users import register_users_callbacks
from .callback_admin import register_admin_callbacks

def register_all_callbacks(dp, log_user_action, db):
    register_users_callbacks(dp, log_user_action, db)
    register_admin_callbacks(dp, log_user_action, db)
