import os
from dotenv import load_dotenv

def load_parameter():
    env = os.getenv("ENV", "dev").lower()

    dotenv_path = ".env.prd" if env == "prd" else ".env.stg"

    load_dotenv(dotenv_path)

    keys = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    return {key: os.getenv(key) for key in keys}