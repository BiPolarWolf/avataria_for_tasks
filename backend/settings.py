# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # секретный ключ для подписи JWT токена
    # openssl rand -hex 32
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # алгоритм подписи JWT токена
    ALGORITHM_ENCRYPT = "HS256"

    # время жизни access JWT токена
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()