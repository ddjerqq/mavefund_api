from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str
    recaptcha_token: str
