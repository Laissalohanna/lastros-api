# config/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    ballants_database_url: str
    delivery_database_url: str
    debug: bool = True

    model_config = {
        "env_file": ".env.prd",
        "env_file_encoding": "utf-8",
    }
