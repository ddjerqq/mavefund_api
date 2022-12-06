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
    __sprinkles = string.ascii_letters + string.digits

    @staticmethod
    def __hash(payload: bytes) -> bytes:
        # return hashlib.sha256(payload.encode()).hexdigest()
        salt = bcrypt.gensalt(8)
        return bcrypt.hashpw(payload, salt)


    @classmethod
    def new(cls, plain_text_password: str) -> str:
        sprinkle = secrets.choice(cls.__sprinkles)
        payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}{sprinkle}"
        return cls.__hash(payload.encode("ascii")).decode("ascii")

    @classmethod
    def compare(cls, hashed_password: str, plain_text_password: str) -> bool:
        for sprinkle in cls.__sprinkles:
            payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}{sprinkle}"

            if bcrypt.checkpw(payload.encode("ascii"), hashed_password.encode("ascii")):
                return True

        return False


# unittest
def test_password_compare():
    password = ''.join(random.choices(string.printable[:-5], k=random.randint(8, 64)))
    password_hash = Password.new(password)
    assert Password.compare(password_hash, password), "passwords do not match"
