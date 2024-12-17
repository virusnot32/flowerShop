from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin: int


@dataclass
class Database:
    name: str


@dataclass
class Config:
    tg_bot: TgBot
    db: Database


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin=int(env('ADMIN_ID')),
        ),
        db=Database(
            name=env('BD_NAME'),
        )
    )
