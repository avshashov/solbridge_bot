from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class SettingsBot(Settings):
    token: str
    parse_mode: str = 'HTML'


class SettingsDB(Settings):
    pg_dsn: str


class SettingsScheduler(Settings):
    trigger: str
    hour: str
    minute: str
    timezone: str


class SettingsPhoto(Settings):
    photo_1: str
    photo_2: str
    photo_3: str
    photo_4: str
