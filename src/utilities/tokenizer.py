from itsdangerous import URLSafeTimedSerializer
import os


def encode_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(os.getenv("PEPPER"))
    return serializer.dumps(email, os.getenv("SALT"))


def decode_token(token: str, expiration: int = 172800):
    serializer = URLSafeTimedSerializer(os.getenv("PEPPER"))
    try:
        email = serializer.loads(
            token,
            salt=os.getenv("SALT"),
            max_age=expiration
        )
        return email
    except Exception as e:
        print(f"exception decoding token: {e}")
        return False
