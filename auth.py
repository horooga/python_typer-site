from passlib.context import CryptContext
from decouple import config
import jwt
import time

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("alghorithm")
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def sign_jwt(nickname: str) -> dict:
    token = jwt.encode({
        "username": nickname,
        "expires": time.time(),
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return { "access_token": token }

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
