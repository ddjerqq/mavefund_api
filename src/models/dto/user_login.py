from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str
    recaptcha_token: str


class ResetPassword(BaseModel):
    email: str


class ResetPasswordVerify(BaseModel):
    password: str
    token: str
