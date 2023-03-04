import os

from aiogram import Bot
from dotenv import load_dotenv


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class SingleBot(Bot):
    def __init__(self):
        load_dotenv()
        super().__init__(token=os.getenv('TOKEN'), parse_mode='HTML')
