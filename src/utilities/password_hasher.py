import os
import string
import hashlib
import secrets


class Password:
    __salt = os.getenv("salt")
    __pepper = os.getenv("pepper")
    __sprinkles = string.ascii_letters + string.digits

    @staticmethod
    def __hash(payload: str) -> str:
        return hashlib.sha256(payload.encode()).hexdigest()

    @classmethod
    def new(cls, plain_text_password: str) -> str:
        sprinkle = secrets.choice(cls.__sprinkles)
        payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}{sprinkle}"
        return cls.__hash(payload)

    @classmethod
    def compare(cls, hashed_password: str, plain_text_password: str) -> bool:
        for sprinkle in cls.__sprinkles:
            payload = f"{cls.__salt}{plain_text_password}{cls.__pepper}{sprinkle}"

            if cls.__hash(payload) == hashed_password:
                return True

        return False
