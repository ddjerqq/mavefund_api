import os
import string
# import hashlib
import bcrypt
import secrets
import random

from dotenv import load_dotenv

load_dotenv()


class Password:
    __salt = os.getenv("SALT")
    __pepper = os.getenv("PEPPER")

    @staticmethod
    def __hash(payload: bytes) -> bytes:
        # return hashlib.sha256(payload.encode()).hexdigest()
        salt = bcrypt.gensalt(8)
        return bcrypt.hashpw(payload, salt)


    @classmethod
    def new(cls, plain_text_password: str) -> str:
        payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}"
        return cls.__hash(payload.encode()).decode()

    @classmethod
    def compare(cls, hashed_password: str, plain_text_password: str) -> bool:
        payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}"

        return bcrypt.checkpw(payload.encode(), hashed_password.encode())


# unittest
def test_password_compare():
    password = ''.join(random.choices(string.printable[:-5], k=random.randint(8, 64)))
    password_hash = Password.new(password)

    assert Password.compare(password_hash, password) is True, "passwords do not match"
