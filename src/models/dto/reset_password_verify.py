from pydantic import BaseModel


class ResetPasswordVerify(BaseModel):
    password: str
    token: str
