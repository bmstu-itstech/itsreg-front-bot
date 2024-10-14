import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Auth:
    secret: str


@dataclass
class Config:
    tg_bot: TgBot
    auth: Auth


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes", "y")


def load_config(path: str):
    config_ = configparser.ConfigParser()
    config_.read(path)

    tg_bot = config_["tg_bot"]

    return Config(
        tg_bot=TgBot(token=tg_bot["token"]),
        auth=Auth(**config_["auth"]),
    )


config = load_config("config.ini")
