import sqlite3

from config_data.config import Config


class Database:
    def __init__(self, config: Config):
        self.conn = sqlite3.connect(config.db.name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flowers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
            """)

            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT
            );
            """)

            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                flower_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (flower_name) REFERENCES flowers (name)
            );
            """)

    def add_flower(self, name):
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO flowers (name) VALUES (?);", (name,))

    def delete_flower(self, name):
        with self.conn:
            self.conn.execute("DELETE FROM flowers WHERE name = ?;", (name,))

    def add_user(self, user_id, first_name, last_name):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (id, first_name, last_name) VALUES (?, ?, ?);",
                (user_id, first_name, last_name)
            )

    def delete_user(self, user_id):
        with self.conn:
            self.conn.execute("DELETE FROM users WHERE id = ?;", (user_id,))

    def add_order(self, user_id, flower_name, quantity):
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO orders (user_id, flower_name, quantity)
                VALUES (?, ?, ?);
                """,
                (user_id, flower_name, quantity)
            )

    def delete_order(self, order_id):
        with self.conn:
            self.conn.execute("DELETE FROM orders WHERE id = ?;", (order_id,))

    def get_statistics(self):
        with self.conn:
            users_count = self.conn.execute("SELECT COUNT(*) FROM users;").fetchone()[0]
            orders_count = self.conn.execute("SELECT COUNT(*) FROM orders;").fetchone()[0]
            return users_count, orders_count

# Пример использования:
# db = Database()
# db.add_flower("Роза")
# db.add_user(123, "Иван", "Иванов")
# db.add_order(123, "Роза", 10)
