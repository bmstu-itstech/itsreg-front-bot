import jwt
import time

from config import load_config

config = load_config("config.ini")


def generate_token(chat_id: int):
    payload = {
        "user_uuid": str(chat_id),
        "expiresAt": int(time.time()) + 2592000,  # for one month
    }
    token = jwt.encode(payload, config.auth.secret, "HS256")
    return token
