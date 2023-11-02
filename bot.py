from aiogram import Bot

from config import SettingsBot

settings_bot = SettingsBot()


class SingleBot(Bot):
    _instances = None

    def __new__(cls):
        if not cls._instances:
            cls._instances = object.__new__(cls)
        return cls._instances

    def __init__(self):
        super().__init__(token=settings_bot.token, parse_mode=settings_bot.parse_mode)
